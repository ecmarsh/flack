document.addEventListener('DOMContentLoaded', () => {
	// Connect to websocket
	var socket = io.connect(
		location.protocol + '//' + document.domain + ':' + location.port
	)

	// When connected, configure buttons
	socket.on('connect', () => {
		// Each button should emit a "submit vote" event
		document.querySelector('#btn-display-name').onclick = () => {
			const displayName = document.querySelector('input#display-name').value
			socket.emit('register display name', { display_name: displayName })
		}
	})

	// When a new vote is announced, add to the unordered list
	socket.on('display name', data => {
		const li = document.createElement('li')
		li.innerHTML = `Display Name: ${data.display_name}`
		document.querySelector('#displayNames').append(li)
	})
})
