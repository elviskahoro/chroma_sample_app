---
title: elvis kahoro - chroma takehome
---
I opened up a PR to fix some small bugs in the docs. TDLR; there was leading whitespace for some of the Python code samples and so the MD parser wasn't registering them correctly as code blocks:

<https://github.com/chroma-core/chroma/pull/3191>

![](/.swm/images/pr-2024-10-25-19-5-51-382.png)

---

The responses to the take-home are below but wanted to share some quick growth opportunities I ran into while working on the app!

## Awesome list

Creating an awesome-repo for Chroma and getting it added to primary Awesome list would be great for growth: <https://github.com/sindresorhus/awesome> (335k stars)

<https://github.com/vinta/awesome-python> (226k stars)

## DLT Integration

DLT ([data load tool](https://dlthub.com/docs/dlt-ecosystem/destinations/)--riffs off of dbt) is a Python framework built on top of Pydantic that helps you parse data sources and load them into destinations (S3, DBs, Snowflake, Vector Databases, etc.). There are destinations for Weaviate, LanceDB, and Qdrant and it'd be great if there was also a Chroma destination!

![](/.swm/images/dlt-plugin-2024-10-25-18-32-59-584.png)

## Quick things I love about the docs

I like the Chroma docs because easy to use, direct, and seem optimized for "time to first app".&nbsp;\
"Edit this page on GitHub" is great for helping people contribute!  It's also nice that the docs are in a subfolder under chroma core so that docs aren't maintained separately!

## Leveraging the Diataxis framework

There's this awesome documentation authoring framework called [Diataxis](https://diataxis.fr/)--"a way of thinking about and doing documentation." They categorize documentation into 4 categories: tutorials, how-to-guides, explanation, and reference docs.

I learned about it a few years back when I read [Docs for developers](https://docsfordevelopers.com/). If there's anyone else that's passionate about docs I'd recommend they read this too.

![](/.swm/images/diataxis-2024-10-25-18-32-8-456.jpg)\
\
Tutorials: "A tutorial serves the user’s *acquisition* of skills and knowledge - their study. Its purpose is not to help the user get something done, but to help them learn."

How-to-guides: "How-to guides are **directions** that guide the reader through a problem or towards a result. How-to guides are **goal-oriented.**"

Reference: **technical descriptions** of the machinery and how to operate it. Reference material is **information-oriented.**

Explanation: "Explanation deepens and broadens the reader’s understanding of a subject.  It’s documentation that it makes sense to read while away from the product itself"

I start writing docs by first mapping the new doc to one of these categories and then use the corresponding outline. A couple of the sample apps could be remixed to have a how-to-guide that demonstrate the use of the APIs that aren't used in the flagship starter example under usage guide!

### Are there plans for a blog?

I think a few blog posts that hit the explanation category and are then hyperlinked / referenced in the docs would be great. Example below:

\
![](/.swm/images/changing%20the%20distance-2024-10-25-18-55-5-790.png)

One might understand how the distance functions are computed but for someone new in the space it's not clear when one outweighs another w.r.t product experience. In what context would using cosine similarity vs Squared L2 lead to a better user experience?\
\
I'd argue Chroma is in a unique position to write such content (you're in-tune with customers and the apps they're building)! The blog post that comes to mind is: "The ideal PR is 50 lines long" from Graphite: <https://graphite.dev/blog/the-ideal-pr-is-50-lines-long>

They're uniquely positioned to share quantitative learnings and best practices about git workflows; and so is Chroma but for AI apps! Graphite is doing a great job with their blog btw, a good source of inspiration: <https://graphite.dev/blog>

![](/.swm/images/guides-2024-10-25-19-21-27-893.png)

## Lightweight docs audit

Would be nice to do a lightweight audit of the docs. Mapping out all of the public chroma endpoints and cross-referencing which ones aren't referenced at all in the docs! The primary deliverable would be making sure the endpoints are referenced appropriately and secondly maybe having an sample app + guide that shows how to use each one.

FastAPI does offer docs when running Chroma locally but my intuition is that people coming from academia backgrounds wouldn't be FastAPI power users nor know they have this out of the box. I think it'd be awesome of this snippet was also included it in the initial usage guide page, right now it's a little bit hidden away behind reference.\
\
The FastAPI docs page helps considerably with local development e.g. can reset the database without halting the process!

![](/.swm/images/fastapi-2024-10-25-19-11-11-171.png)The data loader function is another great candidate!

\
![](/.swm/images/collections-data_loader-2024-10-25-19-29-48-684.png)

# Take home + Feedback

### Improving doc navigation with accordions

The change that I would find the most helpful is restructuring the left sidebar to have expandable accordions for each section. This works best when the docs team is diligent with their use of H2/H3. Being able to expand each section and see the general outline of that page is super helpful with doc navigation and hierarchical search!

I know that the docs currently have a right sidebar and outline, but this requires the user to actually load the page. I often use the sidebar to search for what I'm looking for, see Vercel docs:

![](/.swm/images/vercel-2024-10-25-19-19-59-994.png)

&nbsp;

![](/.swm/images/accordian%20and%20breadcrumbs-2024-10-25-19-24-48-376.png)

### Search

I don't have experience setting up Algolia search myself, so I'm not sure how much customization they provide out of box with their search widget, but it'd be helpful if one could preview the search result they currently have selected. ATM it's difficult to differentiate between the entries because the context window included with each entry is small \~9 words.

![](/.swm/images/algolia%20search-2024-10-25-19-28-56-172.png)

## Dedicated page on filtering i.e. where, etc.

There are some small snippets scattered around the docs on using `where` within a query. A dedicated page on filtering and the best practices around this would be helpful. What all can be filtered, code samples, any limitations on a query with multiple filters, etc.

It's introduced briefly under querying a collection, hyperlinking out to a dedicated filtering page would be helpful here.

![](/.swm/images/where-01-2024-10-25-19-33-33-818.png)\
Similarly, when introducing how to create a collection, the metadata parameter is introduced. The actions we can take on top off metadata however aren't mentioned nor hyperlinked to w.r.t developer experience being able to filter using metadata is helpful and I think this should be emphasized a bit more.

![](/.swm/images/metadata-2024-10-25-19-36-40-339.png)

## Limitations

A dedicated limitations page would also be helpful, maybe even roll into the Troubleshooting and gotcha's page i.e. a single page with a list of the considerations and limitations I need to keep in mind for each primitive. The limitations for the current cloud beta could also be included here.

<p align="center"><img src="/.swm/images/limitations-2024-10-25-19-44-35-526.png"></p>

## Errors and telemetry

I know you have telemetry enabled but I'm wondering whether you're able/also collect error rates. One of the projects that I was going to ramp up but didn't have time to was building out the content for our dedicated error page: <https://reflex.dev/errors/>\
The idea being we prioritize having more in-depth explanations (on the website) for the top errors that people hit and then we include a url to this dedicated error page whenever certain exceptions are raised!

<p align="center"><img src="/.swm/images/Screenshot%202024-11-21-21.52.34-2024-10-25-19-47-6-449.png"></p>

## IDE

It took me a little bit to realize that I should be annotating all off my functions with <SwmToken path="/chroma/chromadb/api/async_api.py" pos="332:2:2" line-data="class AsyncClientAPI(AsyncBaseAPI, ABC):">`AsyncClientAPI`</SwmToken> vs the actual client itself e.g. <SwmToken path="/chroma/chromadb/api/async_client.py" pos="32:2:2" line-data="class AsyncClient(SharedSystemClient, AsyncClientAPI):">`AsyncClient`</SwmToken>&nbsp;\
I'm also still a bit confused on why the client creator functions are standalone public functions vs private functions that are called within **init** sub-methods of each client class; I think the latter would help with the type checking confusion but I'm sure you guys have good reasons--I'm just not yet familiar with them.

```python
class Client(ClientAPI):

    test: str = ""

    @classmethod
    def __init__(
        cls: type[Client],
        host: str = "",
        ...
    ) -> ClientAPI:
        # call the client_creator function here
        # fwiw it is more verbose than the current method

```

Maybe as a stop-gap there could be a short page called Developing with Chroma or Building with Chroma that has some tips and tricks on streamlining the DevX. With some sub-headers for VSCode, Intellij, etc.

![](/.swm/images/chroma-typing%20issues-2024-10-25-19-54-56-388.jpg)

&nbsp;

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBY2hyb21hX3NhbXBsZV9hcHAlM0ElM0FlbHZpc2thaG9ybw==" repo-name="chroma_sample_app"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
