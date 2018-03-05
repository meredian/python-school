var visualizer;

$(function() {
	if (!$('#visualizer_demo').length) {
		return;
	}

	visualizer = new Visualizer('#visualizer_demo', '', '', {'show_stdin_initially': true});
	// visualizer.focusCodeEditor();


	$('#exampleLinks a').click(function(e) {
		visualizer.reset();
		visualizer.setStatus('Загрузка...');

		var loading_status = 0;

		function loaded() {
			loading_status += 1;
			if(loading_status == 2) {
				visualizer.setStatus('');
				// visualizer.run();
			}
		}


		var code_file = $(e.target).data('code');
		var input_file = $(e.target).data('input');

		$.get('/static/example-code/' + code_file, function(code) {
			visualizer.code = code;
			loaded();
		});

		if(typeof(input_file) !== 'undefined') {
			$.get('/static/example-code/' + input_file, function(stdin) {
				visualizer.stdin = stdin;
				loaded();
			});
		} else {
			visualizer.stdin = '';
			loaded();
		}

		return false;
	});

	if (window.gist_urlhash) {
		$.get('/rest_api/gist/', {
			urlhash: window.gist_urlhash
		}, function (data) {
			visualizer.code = data.code;
			visualizer.stdin = data.input_data;
			visualizer.setStatus('');
			visualizer.run();
		});
	} else {
		$('#exampleLinks .default').click();
	}
});

