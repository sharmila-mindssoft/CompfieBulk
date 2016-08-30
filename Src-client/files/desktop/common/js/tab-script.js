
(function() {

	if (!window.sessionStorage.length) {
		localStorage.setItem('getSessionStorage', Date.now());
	};

	window.addEventListener('storage', function(event) {


		if (event.key == 'getSessionStorage') {

			localStorage.setItem('sessionStorage', JSON.stringify(window.sessionStorage));
			localStorage.removeItem('sessionStorage');

		} else if (event.key == 'sessionStorage' && !window.sessionStorage.length) {

			var data = JSON.parse(event.newValue),
						value;

			for (key in data) {
				window.sessionStorage.setItem(key, data[key]);
			}

		}
	});

})();
