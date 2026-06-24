import os

project = "Estudo de Caso: DevSecOps"
author = "Wagner Sousa"
html_title = "Estudo de Caso: DevSecOps"
html_logo = "assets/logo-hb.svg"
extensions = ["myst_parser", "sphinxcontrib.mermaid"]
html_theme = "sphinx_book_theme"
html_theme_options = {
    "show_toc_level": 2,
    "navigation_depth": 3,
}
site_url = os.environ.get("SITE_URL", "").rstrip("/")
if site_url:
    html_theme_options["icon_links"] = [
        {
            "name": "Download PDF (Relatório Final)",
            "url": f"{site_url}/relatorio-final.pdf",
            "icon": "fa-regular fa-file-pdf",
        },
    ]
language = "pt_BR"
exclude_patterns = ["requirements-docs.txt"]
suppress_warnings = ["misc.highlighting_failure"]
