# patent-qa
QA over MatSci patents with GPT-5, with a focus on synthesis. Part of the LLM March Madness Hackathon. 


## Hackathon Admin

[There is a kanban board for collaboration here](https://www.notion.so/Patent-QA-ad3562804e564402a7cc8f80b3ed6f69) (This is public for the duration of the hackathon).

To join the team, just add yourself to the team list below via a PR to this Readme!

## Project Description

A lot of materials synthesis knowledge is locked inside dense patent documents. There is no good way to search these (Google Patent search is not good, ChatGPT is not grounded/truthful without a corpus).

The objective of this hackathon project is to create a pipeline that converts the freely available data from [the US Patent and Trademark Office](https://www.uspto.gov/learning-and-resources/bulk-data-products) that is to do with chemistry/biology/materials science and index it with openai embeddings, and integrate it with e.g Andrew White's Paper QA.

To do this, we’ll need people with experience in large-ish data processing in python, someone interested in building a small frontend on top (optional).


## Data

The download links for the data are here:
https://bulkdata.uspto.gov/

There are many formats, some with images, which are giant. We will ignore these and use the data links under the heading:

*Patent Grant Full Text Data (No Images) (JAN 1976 - PRESENT)*
Contains the concatenated full text of each patent grant document issued weekly (Tuesdays) from January 1, 1976 to present (excludes images/drawings). Subset of the Patent Grant Full Text Data with Embedded TIFF Images. Note: The concatenated file in its entirety is not a valid XML document; it must be un-concatenated back to individual XML documents for XML data processing.

## Rough Plan

- Download the Full Text XML documents from the Patent Office (quite large)
- Write a parser which transforms it into an easy to use format, like a sqlite database.
- Filter the downloaded data to only relevent classes of patents. We could do this using the [Patent Classification System](https://www.uspto.gov/patents/search/classification-standards-and-development) or the Class/Subclass system described in [this delightful PDF](https://www.uspto.gov/sites/default/files/documents/caau.pdf).
- Create a mechanism to chunk these patents into sensible chunks to send to the OpenAI embedding API.
- Write a script to actually do the embedding, and store these in a vector db, such as FAISS or an embedding db which has nice integration with LangChain, like [Chroma](https://github.com/chroma-core/chroma).
- Use the embedding DB to retrieve relevant patents for a user's search, and then use GPT-3/PaperQA to produce high quality, high truthfulness, citable summaries of the data.
- Create a UI around this maybe with hugginface spaces or Vercel if we have people with more full stack experience.

## Alternative ideas

- Google Patents allows you to download a CSV of search results, and links to the raw PDFs. We could create a semi-automated way to scrape and parse these pdfs, allowing "on the fly" processing. This would take a lot longer for a user using our search engine, but would work across a broader set of domains.

- If we have any particular team interests, we could combine papers and patents for a much narrower domain area, e.g Direct Air Capture adsorbents.

### Team

- [Mark Neumann (DeNeutoy)](http://markneumann.xyz)
- Your Name Here!

