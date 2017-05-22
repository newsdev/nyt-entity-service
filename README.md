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
  "dry_run": false
}
```
### Sample response
```
{
  "request": {
    "name": "Bank of America, N.A.",
    "force_create": false,
    "create_if_below": 0.80,
    "dry_run": false
  },
  "response": {
    "name": "Bank of America",
    "match_pct": 0.95,
    "uuid": "ccb4e4c1-b3de-4688-b036-97550c717103"  
  }
}
```
### Required fields
* `entity`, string: The entity name, e.g., `Bank of America` or `Jared Kushner`.

### Optional fields
* `force_create`, boolean: If `true`, will force the creation of a new entity despite the score. Default: `false`. **Note**: This will fail if the name is an EXACT match for another entity in the database. In this case, the exact matching entity will be returned.
* `create_if_below`, float: If the fuzzy match score is below this threshold, a new entity will be created. Default: `0.80`
* `dry_run`, boolean: If `true`, will return without committing any changes to the Entity database. Default: `false`.
*
