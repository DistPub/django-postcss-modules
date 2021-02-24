# django-postcss-modules
Bring `postcss-modules` to your django project, transpiling static .cssm files on the fly, without NodeJS require!

# Install

`pip install django-postcss-modules`

# Static files transpiling config

1. Add `postcss_modules` to your django `INSTALLED_APPS`
1. Add `postcss_modules.middlewares.PostCSSModulesMiddleware` to your django `MIDDLEWARE`
    >note the order
    ```
    [
    ...
    'postcss_modules.middlewares.PostCSSModulesMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ... 
    ]
    ```
1. Config django `STATICFILES_STORAGE = 'postcss_modules.storage.PostCSSModulesStorage'`

# Global Options

Default options is:

```python
{
    'polyfill': 'postcss-modules-v8-polyfill.js',
    'transpiler': 'npm/postcss-modules-standalone@1.0.1/index.bundle.min.js',
    'setup': 'postcss-modules-setup.js',
    'extensions': ['.cssm'],
    'mimetypes': {
        '.cssm': 'text/css'
    },
    'max_time': 3 # transpiling max wait time, in second
}
```

You can customize by provide `POSTCSS_MODULES` in your django settings, for example, custom max time:

```
POSTCSS_MODULES = {
    'max_time': 30
}
```

# Template Support

Sometimes transpiling in your template file is more make sense than static file, 
you can use `postcssmodules` tag to do that.

```
{% load static postcss_modules %}
...
<style id="indexStyles">
{% postcssmodules %}
:global .page {
  padding: 20px;
}

@value hi from '{% static "myapp/css/consts.cssm" %}';

.title {
  composes: title from "{% static "myapp/css/mixins.cssm" %}";
  color: green;
}

.article {
  font-size: 16px;
  color: hi;
}
{% endpostcssmodules %}
</style>
...
<script>
  const _styles = document.querySelector('#indexStyles').sheet
  const styles = JSON.parse(_styles.cssRules[_styles.cssRules.length - 1].style.getPropertyValue('--json'));
  element.innerHTML = '<div class="' + styles.title + '">';
</script>
...
```

Template tag also support use custom transpiling option, for example:

```
{% postcssmodules max_time=30 %}
.title {
  composes: title from "{% static "myapp/css/mixins.cssm" %}";
  color: green;
}
{% endpostcssmodules %}
```
    
# FAQ

1. Static file not get transpiled
    >if you use django `runserver` command to run server and the setting `DEBUG=True`, please add `--nostatic` option to command

1. I want use other storage
    >you should write your own storage to inherit `PostCSSModulesStorage`
