#!/usr/bin/env python

# rdflib_ptgl.py -- Test rdflib with an imaginary RDF vocabulary for the Protein Topology Graph Library (PTGL)
# This is a toy example to try rdflib, ignore.

# Installation of rdflib for this script into separate conda/mamba environment:
#
#  mamba create -n rdflib_ptgl python=3.10
#  conda activate rdflib_ptgl
#  pip install rdflib    # or use conda if you prefer: conda install -c conda-forge rdflib
#

import rdflib

# Create a Graph
g = rdflib.Graph()

# Bind a few prefix, namespace pairs for more readable output
g.bind("ptgl", "http://ptgl.org/ptgl#")


# Create an RDF URI node to use as the subject for multiple triples
ptgl = rdflib.URIRef("http://ptgl.org/ptgl#")

# Add triples using store's add method.
g.add((ptgl, rdflib.RDF.type, rdflib.RDFS.Class))
g.add((ptgl, rdflib.RDFS.label, rdflib.Literal("Protein Topology Graph Library")))
g.add((ptgl, rdflib.RDFS.comment, rdflib.Literal("A library for working with protein topology graphs.")))

# Iterate over triples in store and print them out.
print("--- printing raw triples ---")
for s, p, o in g:
    print((s, p, o))

