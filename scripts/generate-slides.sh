#!/usr/bin/env bash

SCRIPTS_DIR="$(dirname "${BASH_SOURCE}")"
REPO_DIR="${SCRIPTS_DIR}/.."
SLIDES_ADOC="Test management - slides.adoc"
SLIDES_HTML="Test management - slides.html"

pushd "${REPO_DIR}" > /dev/null
    # Make `asciidoctor-revealjs` generate the HTML output.
    npx asciidoctor-revealjs "${SLIDES_ADOC}"
    # Improve indentation with `js-beautify`.
    npx js-beautify --quiet --indent-size=2 --replace "${SLIDES_HTML}"
popd > /dev/null
