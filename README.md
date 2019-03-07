# Hackathon:  Initiating Linked Public Datasets for Agriculture and Food

## Team 1 members:
Simon Jupp, Peter Murray-Rust, Eva Ibarra, Bjoern Oest Hansen

## Intro 

What was your challenge & did you manage to address it?
We call genetically modified events (GM events) to organisms (crops) that have been modified genetically, using conventional breeding or genetic engineering, so they contain genes which confer to the organism the ability to express additional traits or suppress the expression of non desired traits. 
Information about GM events is available in different isolated databases that do not (or rarely) integrate with any other resources. These databases are designed for ‘human users’, meaning that they do not provide any ‘download content’ option or a way to access the database programmatically. Each one of them uses its own vocabulary to define different plant traits. This makes very difficult and tedious for researchers to gather all the existing information about a specific GM event, or to explore the existing gene-enhance/suppress-trait evidences.
In our team, we have tried to integrate three different databases with information about plant traits, genes and GM events. We managed to create a data model that defines the relationships between these main entities. Once that the model was defined, we extracted and standardized the data from the databases. We used these data to feed the model and tested it using some queries. 
Questions we will be able to to answer

Presentation https://docs.google.com/presentation/d/1z0yBN9KYbJ_tY6Bk5nTac0k4RVwEUZPChLHuMSEIeLI/edit#slide=id.p 

## Expected output
 * Neo4j database integrating data from three different databases
 * Set of predefined queries that will result in lists (CSV) or visual output in Neo4j

## Which data did you use / successfully integrate?
* ISAAA GM Database
  Webpage: http://www.isaaa.org/gmapprovaldatabase/default.asp  
  ISAAA presents an easy to use database of Biotech/GM crop approvals for various biotechnology stakeholders. It features the Biotech/GM crop events and traits that have been approved for commercialization and planting and/or for import for food and feed use with a short description of the crop and the trait. Entries in the database were sourced principally from Biosafety Clearing House of approving countries and from country regulatory websites. 

* LMO Registry
  Webpage: https://bch.cbd.int/database/lmo-registry/ 
  The LMO-Unique Identifiers (LMO-UIds) Registry provides summary information on all living modified organisms registered in the BCH including transformation events, genetic modifications, and the unique identification code (if available) for each record. Links to all decisions and Risk assessment reports that refer to these organisms are accessible through the registry. The BCH modalities of operation require the BCH to make use of existing unique identification systems for living modified organisms, as appropriate, to facilitate searching and retrieval of information. 

* OECD BioTrack
  Webpage: https://biotrackproductdatabase.oecd.org/byTrait.aspx 
  OECD public database allows regulatory officials and other interested stakeholders to easily share basic information on products derived from the use of modern biotechnology, as well as some products with novel traits acquired by the use of conventional breeding or mutagenesis, that have been approved for commercial application in at least one country, in terms of food, feed or environmental safety.
  This database accommodates Unique Identifiers, which are intended to be used as "keys" to access information of each transgenic product in this database. The coding system of Unique Identifiers was developed by the OECD Working Group on Biosafety and has since been recognised as an appropriate identification system of products included in the database of Biosafety Clearing House (BCH) of the Cartagena Protocol on Biosafety to the Convention on Biological Diversity as well as in the newly designed FAO GM Foods Platform.

## Implementation 

We used Neo4j as the environment to store our integrated database. It is available here: http://193.62.55.113:7474/browser/ 

Python
Some scripts were used to extract the event info from the databases:

* ISAAA: https://github.com/ebiagridatahackathon/team1/blob/master/scraper/scrape_isaaa.py 
* OECD: https://github.com/ebiagridatahackathon/team1/blob/master/scraper/scrape_biotrack.py 
* LMO: https://github.com/ebiagridatahackathon/team1/blob/master/scraper/scrape_lmo.py 

All extracted data available in this Spreadsheet: https://docs.google.com/spreadsheets/d/1z9KpDA67zo654qesjelG7xbBlFrWoWMp1pd2RBCxL_Y/edit#gid=0 (starts with (1))

# Plant Trait Ontology (from OBO)

We tried to standardize the traits names from the different databases by mapping to the Plant Trait Ontology (https://www.ebi.ac.uk/ols/ontologies/to):
Ontology IRI: http://purl.obolibrary.org/obo/to.owl
Version IRI: http://purl.obolibrary.org/obo/to/releases/2018-09-25/to.owl
Ontology id: to
Version: 2018-09-25
Number of terms: 5093
Last loaded: Wed Sep 26 11:03:46 BST 2018
Trait annotation using ZOOMA
First trait mapping done by Peter, input from OECD database: https://docs.google.com/spreadsheets/d/1uD4sDoCvk-LL6wK9WbCB0wzDgr5EaX8qdvKize-kk2k/edit#gid=0 
Peter: Not many terms mapped successfully onto OBO (ca 9/70)
Simon: mapped more here: https://docs.google.com/spreadsheets/d/1kXwv32pGGBjf9lV3Ur0_c251welKHd0J8XUz9cheyB4/edit#gid=928222895 

# Data Model

Neo4j schema



Neo4j queries

* Retrieve single trait-gene associations: get singular GM events (events that only express one trait and only have one inserted gene). 
`MATCH (g:Gene)--(n:GM_Event)--(t:Trait) return n.id,g.id, collect(distinct(t.id)),count(distinct(t)) order by count(distinct(t)) asc`

* Retrieve all trait-gene information present in the different databases for a specific GM event.
  `MATCH (g:Gene)--(m:GM_Event)--(t:Trait) RETURN m.id,collect(distinct(g.id)),t.id`

 * Get all existing GM events for a particular crop. 
  `MATCH (n:Species)--(g:GM_Event) RETURN n.crop_name,collect(g.id) LIMIT 25`

 * Get all GM events for chemical stress sensitivity (using the trait ontology)
  `MATCH (m:GM_Event)--(t:Trait)-[:type]-(o:Ontology)-[:subclass_of*]->(parents {id : 'TO:0000482'}) RETURN o.label, count(distinct(m.id)) as GM_event`

 * What are the most common trait types for GM events
  `MATCH (m:GM_Event)--(t:Trait)-[:type]-(o:Ontology)-[:subclass_of*]->(parents) RETURN parents.label, count(distinct(m.id)) as GM_event order by GM_event desc`

 * Split GM_ on x into lines 
  `match (g:GM_Event) where not exists((g)--(:Line))
  FOREACH (n in split(g.id, " x ") | merge (g)-[:used_in]-(:Line {id:n}))`
