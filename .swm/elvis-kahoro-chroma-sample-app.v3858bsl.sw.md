---
title: elvis kahoro - chroma sample app
---
I built a small CLI tool that searches through the Bible.&nbsp;\
\
I strongly suggest creating a virtual environment to run the app:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install uv
uv pip install --upgrade pip
uv pip install -r {{requirements_file_path}}
```

I have an ETL pipeline (<SwmPath>[bibledotdev/bibledotdev/pipelines/verses/etl.py](/bibledotdev/bibledotdev/pipelines/verses/etl.py)</SwmPath>) that loads a JSON file with our source data, converts them into a BaseModel and then exports them into a locally running instance of Chroma!\
\
`python -m bibledotdev.pipelines.verses.etl data/staging/verses/json/t_asv.json chroma --count=1000`

<SwmSnippet path="/bibledotdev/bibledotdev/pipelines/verses/etl.py" line="61">

---

The pipeline can be run as a module with parameters that match the primary entry point which is the etl function.

```python
@workflow(
    name="etl",
)
def etl(
    input_file_name: str,
    export_destination: ExportDestinations,
    output_folder: str | None = None,
    count: int | None = None,
) -> None:
    bible_versions: list[BibleVersion] = BibleVersion.load_bible_versions_from_file(
        bible_versions_file_path=Path.cwd() / BIBLE_VERSIONS_FILE_PATH,
    )
    books: list[Book] = Book.load_books_from_file(
        books_file_path=Path.cwd() / BOOKS_FILE_PATH,
    )
    current_bible_version: BibleVersion | None = (
        BibleVersion.filter_bible_version_with_abbreviation(
            bible_version_abbreviation=get_bible_version_abbreviation_from_input_file_name(
                input_file_name=input_file_name,
            ),
            bible_versions=bible_versions,
        )
    )
```

---

</SwmSnippet>

The ETL function calls a helper method for exporting to Chroma, which is located here:<SwmPath>[bibledotdev/bibledotdev/pipelines/verses/export_chroma.py](/bibledotdev/bibledotdev/pipelines/verses/export_chroma.py)</SwmPath>

\
Most of the heavy lifting w.r.t to the cleaning the data is done at the level of each individual model:

<SwmPath>[bibledotdev/bibledotdev/services/app/models/verse.py](/bibledotdev/bibledotdev/services/app/models/verse.py)</SwmPath>

Document models that are meant to be exported into Chroma inherit methods from a Chroma Model ABC:

<SwmPath>[bibledotdev/bibledotdev/services/chroma/models/chroma_document_model.py](/bibledotdev/bibledotdev/services/chroma/models/chroma_document_model.py)</SwmPath>

---

After the data is loaded into Chroma we can query the data using our CLI tool: <SwmPath>[bibledotdev/bibledotdev/cli/\__main_\_.py](/bibledotdev/bibledotdev/cli/__main__.py)</SwmPath>

Searching through verses is run also run as a module similarly to our ETL pipeline.\
`python -m bibledotdev.cli verses search "query text"`

<SwmSnippet path="bibledotdev/bibledotdev/cli/verses/__main__.py" line="52">

---

After querying the search text we display them using a "rich" table for nicer formatting.

```
@app.command()
def search(
    query_text: Annotated[str, typer.Argument()],
    count: Annotated[int, typer.Argument()] = 10,
    app_connection_state_raw: Annotated[bool, typer.Argument()] = False,
) -> None:
    argument_type_str: str = __name__
    if not is_valid_argument(
        argument_type_str=argument_type_str,
        argument_type_enum=SearchTypes,  #  trunk-ignore(pyright/reportArgumentType)
    ):
        raise is_invalid_argument_exception(
            argument_type_str=argument_type_str,
            argument_type_enum=SearchTypes,  # trunk-ignore(pyright/reportArgumentType)
        )

    app_connection_state: AppConnectionStateType = (
        AppConnectionStateType.IS
        if app_connection_state_raw
        else AppConnectionStateType.IS_OFFLINE
    )
    chroma_client: ClientAPI = aiorun(
        main=get_client_chroma(
            app_connection_state=app_connection_state,
            tokens=TOKENS,
            client_type=ClientType.SYNC,
        ),
    )

    collection_name: str = "verses"
    collection: Collection = chroma_client.get_collection(
        name=collection_name,
    )
    typer.echo(
        message=f"Collection: {collection_name} count: {collection.count()}",
    )
    query_result: QueryResult = collection.query(
        query_texts=[query_text],
        n_results=count,
    )
    table = Table(
```

---

</SwmSnippet>

I plan to eventually build some proper UI using [Reflex](https://reflex.dev/) to eventually host this as a web app. I also need to investigate a bug with some of the text highlighting for the console output--currently I have it set to highlight any keywords from the query text but it seems to not work for every line.

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBY2hyb21hX3NhbXBsZV9hcHAlM0ElM0FlbHZpc2thaG9ybw==" repo-name="chroma_sample_app"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
