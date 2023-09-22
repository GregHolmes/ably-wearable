const express = require('express')
const cors = require('cors')
const path = require("path")
const Ably = require('ably')
const bodyParser = require('body-parser')

require('dotenv').config()

var client = new Ably.Rest(process.env.ABLY_API_KEY)
var channel = client.channels.get(process.env.ABLY_CHANNEL)

const port = 8080

const app = express()

app.use(cors())
app.use(express.json())

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(express.urlencoded({ extended: true }))
app.use(express.static(path.join(__dirname, 'public')))

app.set('trust proxy', true)

app.get("/", (req, res) => {
  res.render("index", { title: "Home" })
})

app.post("/", (req, res) => {
  const message = req.body.message

  channel.publish('message', message, function(err) {
    if (err) {
      res.render("index", { status: "error" })
    } else {
      res.render("index", { status: "success" })
    }
  })
})

app.set("views", path.join(__dirname, "views"))
app.set("view engine", "pug")

app.listen(port, () => {
  console.log(`Demo app listening at http://localhost:${port}`)
})
