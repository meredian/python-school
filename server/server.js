const path = require('path');

const connect = require('connect');
const serveStatic = require('serve-static');
const morgan = require('morgan');
const request = require('request');
const bodyParser = require('body-parser')

const PORT = process.env.PORT || 3000;

const staticResources = serveStatic(path.join(__dirname, 'static'), {
    index: false,
});

const staticPages = serveStatic(path.join(__dirname, 'pages'), {
    index: ['index.html'],
});

connect()
    .use(morgan('short'))
    .use(bodyParser.urlencoded({extended: true}))
    .use('/visualizer/execute', (req, res, next) => {
        request({
            uri: 'http://pythontutor.ru/visualizer/execute/',
            method: 'POST',
            headers: {
                Host: 'pythontutor.ru',
                Referer: 'http://pythontutor.ru/',
                DNT: req.headers.DNT,
                'X-Requested-With': req.headers['X-Requested-With'],
            },
            form: req.body,
        }).pipe(res);
    })
    .use('/static', staticResources)
    .use('/', staticPages)
    .listen(PORT);

console.log(`Listening on port ${PORT}.`);