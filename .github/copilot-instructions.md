# Copilot Instructions for messer-gtm-troubleshoot

## Project Overview
This codebase is focused on troubleshooting, analyzing, and visualizing Google Tag Manager (GTM) and related data for the Messer project. It contains HTML dashboards, Python scripts, and large JSON/CSV data dumps for audit and debugging purposes.

## Key Components
- **HTML Dashboards**: Files like `action-plan.html`, `audit-board.html`, `canvas-graph.html`, and others provide visualizations and interactive tools for GTM analysis.
- **Python Scripts**: The main script is `chunk_wgtm_files.py`, which processes and chunks large GTM-related data files for easier analysis.
- **Data Dumps**: The `chunked_output/` directory contains chunked JSON files, likely produced by the Python script, representing segmented GTM message logs.
- **Raw Data**: Files such as `messer datalayers new.txt`, `stape io logs messer.csv`, and various GTM workspace JSONs are used as input for analysis and troubleshooting.

## Developer Workflows
- **Data Processing**: Run `chunk_wgtm_files.py` to process large GTM logs into manageable chunks. Example command:
  ```bash
  python chunk_wgtm_files.py
  ```
- **Visualization**: Open the HTML files in a browser to view dashboards and analysis tools. No build step is required; these are static files.
- **Adding New Data**: Place new GTM logs or workspace exports in the root or `chunked_output/` directory, then re-run the Python script if chunking is needed.

## Project-Specific Patterns
- **Chunked Data**: Large GTM message logs are split into numbered JSON files for performance and easier inspection.
- **Loose Coupling**: There is no tight integration between scripts and dashboards; data is processed separately and then visualized.
- **No Frameworks**: The project does not use web frameworks or package managers. All HTML is static, and Python scripts are standalone.

## Integration Points
- **External Data**: Integrates with GTM via exported workspace JSONs and logs from tools like Tag Assistant and Stape.io.
- **Manual Data Flow**: Data is manually moved between scripts and dashboards; automation is minimal.

## Conventions
- **File Naming**: Chunked files follow the pattern `tag_assistant_<source>_messages_chunk_<N>.json`.
- **Directory Structure**: All analysis and visualization tools are in the project root; chunked data is in `chunked_output/`.
- **No Tests**: There are no automated tests or CI/CD workflows present.

## Examples
- To process new GTM logs: Add the file, run the Python script, and view results in the HTML dashboards.
- To extend analysis: Add new Python scripts or HTML files following the existing patterns.

## References
- Main script: `chunk_wgtm_files.py`
- Data directory: `chunked_output/`
- Dashboards: `*.html` in project root

---
For questions or improvements, document new patterns in this file to help future AI agents and developers.
