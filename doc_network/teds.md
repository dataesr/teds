---
title: "Mapping scientific communities at scale"
author:
  - Hafsa Aallat:
      institute: mesr

institute:
  - mesr:
      name: "French Ministry of Higher Education and Research, Paris, France"
bibliography: teds.bib
date: February 2025
keywords:
  - French publications
  - Machine learning
  - scanR
  - OpenAlex
  - Biblioglutton
  - Elasticsearch
geometry: "left=3cm, right=3cm, top=3cm, bottom=3cm"
---

**Keywords**: open access, open science, open data, open source

# Abstract

# 1. Motivation

## 1.1 Presentation of IPCC and IPBES: Working Groups and dates

**The IPCC (Intergovernmental Panel on Climate Change)** assesses scientific information on climate change, providing reports to guide policymakers. It has three working groups sees as three main themes :

- Working Group I (WGI) focuses on the **physical science** of climate change.
- Working Group II (WGII) examines climate change impacts, **adaptation**, and vulnerabilities.
- Working Group III (WGIII) addresses climate change **mitigation** strategies.
  The Sixth Assessment Report (AR6) was released in stages between 2021 and 2022.

**The IPBES (Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services)**, established in 2012, assesses biodiversity and ecosystem services. It produces thematic and regional assessments, with the **Global Assessment Report (2019)** highlighting biodiversity loss and the need for urgent action.
Both platforms provide crucial scientific assessments that inform global climate and biodiversity policies.

## 1.2 Limits of the French Court of Auditors study

In 2023, the French Court of Auditors conducted a study on France's scientific output related to environmental transition. After hearings with the Directorate General for Research and Innovation (DGRI) and research operators, the Court analyzed the bibliography cited in the sixth IPCC report. The study found that French publications are most cited in the physical sciences of climate change, highlighting the global impact of French research in this field.

However, this evaluation has important limitations. The IPCC bibliography, while rigorously selected, is based on high-impact publications often from top journals, making it inherently selective. This selection prioritizes more visible and well-known works, leaving out other important research that may not be as prominent but still highly relevant and in the same themes as IPCC report. While this reflects France's scientific excellence, it does not fully represent the diversity and breadth of French scientific contributions to ecological transition.

To address this gap, we propose using a larger dataset, such as scanR. ScanR has a significantly higher coverage of publications with at least one French affiliation compared to other sources, contributing 92% to the overall aggregated corpus. This is much higher than databases like Scopus (67%), WoS (58%), or PubMed (29%), making ScanR a more comprehensive tool for capturing French scientific publications.[@10.1162/qss_a_00179]
Unlike the IPCC's restricted approach, ScanR includes publications with at least one French affiliation, offering a broader view of research. This will allow us to capture a more diverse range of topics related to climate change adaptation and mitigation, as well as uncover valuable contributions that may be overlooked in narrower studies.

Initially, we will replicate the Court of Auditors' analysis of the IPCC bibliography to identify the main themes and their proportion of French contributions. Then, we will expand our study to include all French publications in the field, focusing on the institutions, labs, regions, and researchers most involved, and also highlighting contributions that provide solutions to the challenges of environemental solutions. At the same time, we will conduct a similar analysis for the IPBES bibliography, following the same approach to identify the main themes and French contributions, and exploring less visible but valuable research related to biodiversity and ecosystem services.

# 2. Network analysis at scale

We propose a method for overcoming the limitations set out above. We also use a filtering technique to reduce the size of the network, but with a dual approach: instead of filtering the nodes, we filter the links.

## 2.1 Focusing on strongest interactions

One of the added values of mapping with a network view is to show the interactions between entities, i.e. the links between the nodes in the graph. These links provide crucial information that can be used to structure communities. If the size of the network needs to be reduced (for reasons of computation, speed, legibility and interpretability), it is vital to preserve the links that carry the most information, i.e. the strongest interactions. With this reasoning, it seems logical to reduce the size of the network by only affecting the strongest links.

Thus, from a given corpus, however large, we seek to extract the pairs of entities with the strongest interactions, for example the most co-signatures per pair of authors. From this list of pairs, we can naturally find the nodes of the graph and deduce a new graph. If the graph has several independent components, i.e. several unconnected sub-graphs, we can decide to keep only the main component(s).

## 2.2 Elasticsearch implementation

To identify the strongest links, it would be too costly to go through the entire corpus. We have pre-calculated the links at the level of each publication. So, if a publication is linked to 3 themes, T1, T2 and T3, a pre-calculated field, at publication level, contains all T1-T2, T1-T3 and T2-T3 pairs. This co_topics field represents the co-appearance links within the publication. We then use elasticsearch's aggregation functionality to list the most present links, very efficiently.

In practice, a PID is also stored (the wikidata for topics, for example) to disambiguate entities. In practice, for a given query, elasticsearch returns a response containing the strongest links, for example:

```json
                {
                    "key": "Q15305550###carbon sequestration---Q7942###climate change",
                    "doc_count": 17,
                },
                {
                    "key": "Q15305550###carbon sequestration---Q623###carbon",
                    "doc_count": 14,
                },
                {
                    "key": "Q15305550###Carbon sequestration---Q7942###Climate change",
                    "doc_count": 13,
                },
                {
                    "key": "Q15305550###Carbon sequestration---Q898653###Climate change mitigation",
                    "doc_count": 10,
                },
                {
                    "key": "Q397350###agroforestry---Q8486###coffee",
                    "doc_count": 10,
                },
                {
                    "key": "Q15305550###Carbon sequestration---Q1997###CO2",
                    "doc_count": 9,
                },
                {
                    "key": "Q623###carbon---Q627###nitrogen",
                    "doc_count": 9,
                },
                {
                    "key": "Q15305550###Carbon sequestration---Q623###carbon",
                    "doc_count": 7,
                },
```

## 2.3 VOSviewer implementation

We use the open source VOSviewer online tool for network visualization [https://github.com/neesjanvaneck/VOSviewer-Online](https://github.com/neesjanvaneck/VOSviewer-Online). It is based on the VOSviewer tool which is very popular for network analysis in bibliometric studies [@DBLP:journals/corr/abs-1006-1032].

## 2.4 LLM trick

# 3. Making insightful maps

## 3.1 why scanR ?

ScanR has a significantly higher coverage compared to other sources, contributing 92% to the overall aggregated corpus. This is much higher than databases like Scopus (67%), WoS (58%), or PubMed (29%), making ScanR a more comprehensive tool for capturing French scientific publications.[@10.1162/qss_a_00179]

## 3.2 Custom perimeter

scanR offers this mapping tool for the entire indexed corpus, but it is also possible to adapt the tool to a restricted perimeter, at the user's discretion. For example, an institution or laboratory can define its own corpus (based on a list of publications) and a mapping tool dedicated to this perimeter is automatically created. Technically, elasticsearch queries are the same, with just an additional filter to query only the publications within the perimeter. The tool can be embedded in any website using an iframe. It's the same principle as the local barometer. This approach eliminates the need for automatic alignment of affiliations, which remains a highly complex task. Automation is possible to a certain extent [@lhote_using_2021], but human curation remains necessary in the majority of cases [@jeangirard:hal-04598201]. In this way, users retain control over the definition of their perimeter, and can, if they wish, have several distinct perimeters.

# 4. Code availibility

The code developed for the scanR web application is open source and available online on GitHub [https://github.com/dataesr/scanr-ui](https://github.com/dataesr/scanr-ui)

# References
