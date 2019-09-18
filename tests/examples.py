# -*- coding: utf-8 -*-

"""Example BEL scripts."""

__all__ = [
    'simple',
]

simple = """##################################################################################
# Document Properties Section

SET DOCUMENT Name = "PyBEL Test Simple"
SET DOCUMENT Description = "Made for testing PyBEL parsing"
SET DOCUMENT Version = "1.6.0"
SET DOCUMENT Copyright = "Copyright (c) Charles Tapley Hoyt. All Rights Reserved."
SET DOCUMENT Authors = "Charles Tapley Hoyt"
SET DOCUMENT Licenses = "WTF License"
SET DOCUMENT ContactInfo = "cthoyt@gmail.com"
SET DOCUMENT Project = "PyBEL Testing"

##################################################################################
# Definitions Section

DEFINE NAMESPACE CHEBI AS URL \
"https://owncloud.scai.fraunhofer.de/index.php/s/JsfpQvkdx3Y5EMx/download?path=chebi.belns"
DEFINE NAMESPACE HGNC AS URL \
"https://owncloud.scai.fraunhofer.de/index.php/s/JsfpQvkdx3Y5EMx/download?path=hgnc-human-genes.belns"
DEFINE ANNOTATION Species AS \
URL "https://owncloud.scai.fraunhofer.de/index.php/s/JsfpQvkdx3Y5EMx/download?path=species-taxonomy-id.belanno"
DEFINE ANNOTATION CellLine AS \
URL "https://owncloud.scai.fraunhofer.de/index.php/s/JsfpQvkdx3Y5EMx/download?path=cell-line.belanno"

##################################################################################
# Statements Section

SET STATEMENT_GROUP = "Group 1"

SET Citation = {"PubMed","That one article from last week","123455","2012-01-31","Example Author|Example Author2"}
SET Species = "9606"

SET Evidence = "Evidence 1 \
w extra notes"

p(HGNC:AKT1) -> p(HGNC:EGFR)

SET Evidence = "Evidence 2"
SET CellLine = "10B9 cell"

p(HGNC:EGFR) -| p(HGNC:FADD)
p(HGNC:EGFR) =| p(HGNC:CASP8)

SET Citation = {"PubMed","That other article from last week","123456"}
SET Species = "10116"
SET Evidence = "Evidence 3"

p(HGNC:FADD) -> p(HGNC:CASP8)
p(HGNC:AKT1) -- p(HGNC:CASP8)
"""
