# Interview assignment

## Usage

```
<init you virtualenv>
pip install -r ./requirements.txt
uvicorn search:app --reload
```

Documentation is available under `http://localhost:8000/docs`.


## Progress

- [x] Use type annotations and schemas
- [x] Query backend in parallel
- [x] Put depenencies in requirements
- [] Write some tests
- [x] Autoformart (isort and black)
- [x] Flake8
- [] ui
- [] deployment
- [] security hardening
- [] self.session: The object should be created from async function


## Things that could be done better

1. Documentation.
1. Requirements could benefit from using `pip-tools`.
1. Exception hierarchy.
1. Better error handling.
1. Possibly "streaming" API from integrations.
1. `Limit` and `order` parameters for search endpoint.
1. Tests should not talk to the Internet.
1. Code layout.
1. `/available-engines` returns a list as a top json object.

## Task Description

At Office App we like to see ourselves as an integration company, we act as a layer between several third-party integrations and the end-user. Providing a uniform data format through our API, independently of the used integrations.

For this case, we would like you to build a mini API that functions as a layer between an application and several integrations. With this API it should be possible to search public repositories on a hosting platform for version control using Git. For example Gitlab, Github, or Bitbucket. The API should at least provide one endpoint which can be used to search for repositories. It should be possible to search within different integrations (so hosting platforms).
We leave it up to you how you would like to build it. Obviously, there are a few things we like to see though:


- A API endpoint to search for repositories

- Unit testing for this endpoint

- At least one connected integration, so searching through Gitlab repositories for example.

- A uniform, integration independent response format

- Documentation on how the API can be set up and used

- Documentation on what is achieved, what could be done better (with more time and resources), lessons learned, and possible difficulties you have encountered.

## Additional Comments

> With search we mean a simple search phrase with which you would like to find matching repositories. For example a search on the repository title. Other 'attributes' can be searched as well, that is up to you and time.
>
> For output it is important it is uniform, independently of the integration being used. What attributes (title, code, tags etc.) you would like to include in the response is up to you. Hopefully this answers your question, otherwise, please let me know!’