# NYT Entity Service
A web service for disambiguating entities.

Your application can POST some JSON to the service with a name to match and some optional flags describing how to process your request. The service will return a UUID that will uniquely identify this entity across a variety of applications.

Alternately, if you're writing Python, you can use [our entity uploader](https://github.com/newsdev/nyt-entity-uploader).

**Coming soon**: An admin interface for combining / deduplicating entities and for searching / exploring entities.

## Usage
### Example: Entity Uploader
See [the entity uploader docs](https://github.com/newsdev/nyt-entity-uploader) for more.

### Example: Raw JSON
#### Required fields
* `name`, string: The entity's name, e.g., `Bank of America` or `Jared Kushner`.

#### Optional fields
* `create_if_below`, integer, 0-100: If the fuzzy match score is below this threshold, a new entity will be created. Default: `80`

#### POST data
```
{
  "name": "Bank of America N.A.",
  "create_if_below": 80,
}
```
#### Response data
```
{
  "request": {
    "name": "Bank of America, N.A.",
    "create_if_below": 80,
  },
  "response": {
    "name": "Bank of America",
    "score": 95,
    "uuid": "ccb4e4c1-b3de-4688-b036-97550c717103",
    "created": false
  }
}
```
