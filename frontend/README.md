# Frontend

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
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


