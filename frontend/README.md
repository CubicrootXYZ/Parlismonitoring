# Frontend

Vue 3 page that taks to the API.

## Troubleshooting

**Can not find ../package.json**

Start with sleep container and:

```
npm rebuild
```

**Website shows: Invalid Header**

Add a vue.config.js to main directory with:

```
module.exports = {
    devServer: {
        disableHostCheck: true
    }
}
```

## Project setup
Adapt the `/src/main.js` to your needs. Set the api's url and the webpages url.

```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production

An example Dockerfile for production use is provided within this repository.

```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


