const clientId = 'mqttjs_' + Math.random().toString(16).slice(2, 8)

const mqttHost = document.getElementById("MQTT_HOST").value || 'localhost'
const mqttWSPort = document.getElementById("MQTT_WS_PORT").value || '8083'

const host = 'ws://' + mqttHost + ':' + mqttWSPort +'/mqtt'

const options = {
  keepalive: 60,
  clientId: clientId,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
  will: {
    topic: 'WillMsg',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false
  },
}

console.log('Connecting mqtt client ' + host)
const client = mqtt.connect(host, options)
client.on('connect', () => {
  console.log(`Client connected: ${clientId}`)
  // Subscribe
  client.subscribe('ui/deposit', { qos: 0 })
  client.subscribe('ui/factory', { qos: 0 })
})
client.on('message', (topic, message, packet) => {
  const parsed = JSON.parse(message)
  if (topic === 'ui/deposit')
    process_deposit(parsed)
  else if (topic === 'ui/factory')
    process_factory(parsed)
})
client.on('error', (err) => {
  console.log('Connection error: ', err)
  client.end()
})
client.on('reconnect', () => {
  console.log('Reconnecting...')
})

function process_deposit(parsed) {
  const qtdProducts = Object.keys(parsed).length || 0
  document.getElementById(
    'produced-products'
  ).innerText = qtdProducts.toString()
}

function process_factory(parsed) {
  const ulRed = document.getElementById("red-factory")
  const ulYellow = document.getElementById("yellow-factory")
  const ulGreen = document.getElementById("green-factory")
  ulRed.innerHTML = "";
  ulYellow.innerHTML = "";
  ulGreen.innerHTML = "";
  
  Object.keys(parsed).forEach((key) => {
    let li = document.createElement('li')
    li.appendChild(document.createTextNode(key.toString()))
    if (parsed[key].level == 'red')
      ulRed.appendChild(li)
    else if (parsed[key].level == 'yellow')
    ulYellow.appendChild(li)
    else if (parsed[key].level == 'green')
    ulGreen.appendChild(li)
  })
}
