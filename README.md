# NYT Entity Service
A web service for disambiguating entities.

You can post some JSON to the service with a name to match and some optional flags describing how to process your request.

The service will return a UUID that will uniquely identify this entity across all INT / CAR applications.

There's also an admin interface for combining / deduplicating entities and for searching / exploring entities.

## Usage
### Sample request
```
{
  "name": "Bank of America N.A.",
  "force_create": false,
  "create_if_below": 0.80,
}
```
### Sample response
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
### Required fields
* `entity`, string: The entity name, e.g., `Bank of America` or `Jared Kushner`.

### Optional fields
* `create_if_below`, integer: If the fuzzy match score is below this threshold, a new entity will be created. Default: `80`
