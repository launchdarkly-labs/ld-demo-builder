# LD Demo Builder for Coast Demos

## Run Lambda URL

To create a demo environment:

Method: `POST`
Body: 
```
{
    "action": "build"
}
```

To remove a demo environment:

Method: `POST`
Body: 
```{
    "action": "cleanup"
    "project-key": "cxld-project-key"
}
```
