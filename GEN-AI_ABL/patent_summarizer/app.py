"""
Streamlit Web App for Patent Claim Summarizer & Novelty Extractor

Integrates USPTO, EPO, and Google BigQuery datasets with retrieval and LLM analysis.
"""

import streamlit as st
import logging
import sys
import os
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import project modules
from pipeline import PatentAnalysisPipeline
from retriever import BruteForceRetriever, TFIDFRetriever
from data_ingestion.ingest_and_run import ingest_from_uspto, ingest_from_epo, ingest_from_bigquery, load_local_samples

st.set_page_config(page_title="Patent Summarizer & Novelty Extractor", page_icon="📄", layout="wide")


def inject_theme_css():
        """Inject polished theme CSS into Streamlit page."""
        primary = "#4A90E2"
        success = "#28A745"
        accent = "#6C63FF"
        bg = "#F7FAFC"
        card_bg = "#FFFFFF"
        css = f"""
        <style>
        :root {{
            --primary: {primary};
            --success: {success};
            --accent: {accent};
            --bg: {bg};
            --card: {card_bg};
        }}
        /* Page background */
        .stApp {{ background-color: var(--bg); }}
        /* Card */
        .card {{
            background: var(--card);
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 4px 18px rgba(20,20,30,0.06);
            margin-bottom: 12px;
        }}
        .card h3 {{ margin-top: 0; }}
        /* Buttons */
        .stButton>button {{
            background: linear-gradient(180deg, var(--primary), #357ABD);
            color: white;
            border-radius: 10px;
            padding: 8px 14px;
            box-shadow: none;
            border: none;
        }}
        /* Success banner */
        .success-banner {{
            background: linear-gradient(90deg, rgba(40,167,69,0.06), rgba(106,197,104,0.04));
            border-left: 4px solid var(--success);
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        /* Smaller text for metadata */
        .muted {{ color: #6b7280; font-size: 0.9rem; }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)


inject_theme_css()

def load_retriever(index_dir: str):
    """Load retriever from index directory, trying TF-IDF first then BruteForce."""
    try:
        retriever = TFIDFRetriever.from_metadata(index_dir)
        st.info("Using TF-IDF retriever")
        return retriever
    except Exception as e:
        st.warning(f"TF-IDF not available ({e}), falling back to BruteForce")
        try:
            retriever = BruteForceRetriever.load_from_dir(index_dir)
            st.info("Using BruteForce retriever")
            return retriever
        except Exception as e2:
            st.error(f"Failed to load retriever: {e2}")
            return None

def load_prior_art(source: str, limit: int = 50):
    """Load prior art from selected source."""
    if source == "USPTO":
        return ingest_from_uspto(limit=limit)
    elif source == "EPO":
        return ingest_from_epo(limit=limit)
    elif source == "Google BigQuery":
        return ingest_from_bigquery(limit=limit)
    elif source == "Local Samples":
        return load_local_samples(limit=limit)
    else:
        return []

def main():
    st.title("📄 Patent Claim Summarizer & Novelty Extractor")
    st.markdown("""
    Analyze patent claims for summaries, novelty, and overlaps with prior art.
    Supports USPTO, EPO, and Google Patents datasets.
    """)

    # Sidebar for configuration
    st.sidebar.header("Configuration")

    # Data source selection
    data_source = st.sidebar.selectbox(
        "Select Data Source for Prior Art",
        ["Local Samples", "USPTO", "EPO", "Google BigQuery"],
        help="Choose the dataset to use for prior art retrieval"
    )

    # Index directory
    index_dir = st.sidebar.text_input(
        "Index Directory",
        "data/indices/uspto_sample_100",
        help="Directory containing embeddings.npy and metadata.pkl"
    )

    # Analysis style
    style = st.sidebar.selectbox(
        "Analysis Style",
        ["technical", "legal", "layperson"],
        help="Style for summary and novelty analysis"
    )

    # LLM mode
    use_mock_llm = st.sidebar.checkbox(
        "Use Mock LLM",
        value=True,
        help="Use mock LLM for demo (faster, no GPU required)"
    )

    # Main content
    st.header("Patent Input")

    col1, col2 = st.columns(2)

    with col1:
        patent_id = st.text_input("Patent ID", "SAMPLE-001")
        title = st.text_input("Title", "Advanced Machine Learning System")
        abstract = st.text_area("Abstract", "A novel system for processing data using machine learning techniques.")

    with col2:
        description = st.text_area("Description", "The invention relates to ML systems and describes input processing and neural network layers.")
        claims_text = st.text_area("Claims Text", "1. A method comprising: receiving data; processing the data; outputting results.\n2. The method of claim 1, wherein the processing comprises neural networks.")

    # Analysis button
    if st.button("Analyze Patent", type="primary"):
        with st.spinner("Loading retriever and prior art..."):
            # Load retriever
            retriever = load_retriever(index_dir)
            if retriever is None:
                st.error("Failed to load retriever. Check index directory.")
                return

            # Load prior art
            prior_art = load_prior_art(data_source, limit=50)
            if not prior_art:
                st.warning("No prior art loaded. Using empty database.")

        with st.spinner("Running analysis..."):
            # Create pipeline
            pipeline = PatentAnalysisPipeline(use_mock_llm=use_mock_llm)
            pipeline.set_retriever(retriever)
            pipeline.set_prior_art_database(prior_art)

            # Prepare patent data
            patent_data = {
                'patent_id': patent_id,
                'title': title,
                'abstract': abstract,
                'description': description,
                'claims_text': claims_text
            }

            # Run analysis
            try:
                result = pipeline.analyze_patent(patent_data, claim_number=1, style=style)

                # Display results with polished cards and export buttons
                st.markdown('<div class="success-banner">Analysis complete — results are ready.</div>', unsafe_allow_html=True)

                st.header("Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown('<div class="card"><h3>Summary</h3>', unsafe_allow_html=True)
                    st.write(result.summary)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="card"><h3>Novelty</h3>', unsafe_allow_html=True)
                    st.write(result.novelty)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="card"><h3>Overlaps</h3>', unsafe_allow_html=True)
                    st.write(result.overlaps)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Prior art used
                st.subheader("Prior Art Retrieved")
                if getattr(result, 'prior_art_used', None):
                    for pa in result.prior_art_used[:5]:  # Show top 5
                        with st.expander(f"Patent {pa.get('patent_id', 'N/A')}"):
                            st.write(f"Abstract: {pa.get('abstract', '')}")
                else:
                    st.write("No prior art retrieved.")

                # Provide JSON/CSV exports of the analysis
                try:
                    import json
                    import io

                    try:
                        result_dict = result._asdict()
                    except Exception:
                        result_dict = getattr(result, '__dict__', None) or {
                            'summary': str(getattr(result, 'summary', '')),
                            'novelty': str(getattr(result, 'novelty', '')),
                            'overlaps': str(getattr(result, 'overlaps', ''))
                        }

                    json_bytes = json.dumps(result_dict, ensure_ascii=False, indent=2).encode('utf-8')
                    st.download_button("Download JSON", data=json_bytes, file_name=f"{patent_id}_analysis.json", mime="application/json")

                    # CSV: simple key,value rows
                    csv_buf = io.StringIO()
                    for k, v in result_dict.items():
                        # flatten simple values
                        csv_buf.write(f'"{k}","{str(v).replace(chr(34), "'")}"\n')
                    st.download_button("Download CSV", data=csv_buf.getvalue(), file_name=f"{patent_id}_analysis.csv", mime="text/csv")
                except Exception as e:
                    logger.debug(f"Export buttons failed: {e}")

            except Exception as e:
                st.error(f"Analysis failed: {e}")
                logger.exception("Analysis error")

    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit, Transformers, FAISS, and open-source LLMs.")

if __name__ == "__main__":
    main()
