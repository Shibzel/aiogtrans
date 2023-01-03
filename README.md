# Aiogtrans
An asynchronous and unlimited library done on the fly for google translate.

### Example of usage

```python
from aiogtrans import GoogleTrans

# Must be inside of an async func
async with GoogleTrans(target="fr") as translator:
    result = await translator.translate("Hello everyone !")
    print(result.text)
    detected_language = await translator.detect("Ich mag Wasser")
    print(detected_language)
```

Output :

```
Bonjour à tous !
('deutch', 'de')
```
