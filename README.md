# Aegis image annotator node

## Usage
POST
```js
{
  image: "<base64 encoded image>",
  annotations: [
    {
      bounds: [x, y, w, h],
      text: "hello world", //optional
      color: "#88ffaa" //optional
    }
    ...
  ]
}

```
to `/` to get a list of bounds and confidences like so:
```js
[
  {
    bounds: [x, y, w, h],
    confidence: 0.99
  }
  ...
]
```

## Environment
- `PORT` - the port to listen on

## TODO
- allow for adjustable font face and size
