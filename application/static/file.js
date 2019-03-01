var geturl = window.location.href;
$(document).ready(function(){
	if(geturl=="http://localhost:5000/upload")
	{
	var image = document.getElementById('slika');
	image.src = "/static/pictures/original.jpg";
	}
	
	$('#brightness').change(function(){
	var text = '{ "brightness" : "' + $('#brightness').val()  + '" , "contrast" : "' + $('#contrast').val()+ '" }' ;
		var image = document.getElementById('slika');
        $.ajax({
                type: 'POST',
				url: '/brightness_and_contrast',
				dataType: "json",
				data: text
				}).done(function(response) {
					image.src = response['image_path'];
				});
	});

	
	$('#contrast').change(function(){
			var text = '{ "brightness" : "' + $('#brightness').val()  + '" , "contrast" : "' + $('#contrast').val()+ '" }' ;
			var image = document.getElementById('slika');
			$.ajax({
					type: 'POST',
					url: '/brightness_and_contrast',
					dataType: "json",
					data: text
					}).done(function(response) {
						image.src = response['image_path'];
					});
		});

	$('#surface').change(function(){
		var text = '{ "shape" : "' + $('#shape').val() + '" , "color" : "' + $('#color').val() +
		'" , "surface" : "' +$('#surface').val() + '" }' ;
		var image = document.getElementById('slika');
        $.ajax({
                type: 'POST',
				url: '/geometry',
				dataType: "json",
				data: text
				}).done(function(response) {
					image.src = response['image_path'];
				});
	});

	
	$('#color').change(function(){
		var text = '{ "shape" : "' + $('#shape').val() + '" , "color" : "' + $('#color').val() +
		'" , "surface" : "' +$('#surface').val() + '" }' ;
		var image = document.getElementById('slika');
        $.ajax({
                type: 'POST',
				url: '/geometry',
				dataType: "json",
				data: text
				}).done(function(response) {
					image.src = response['image_path'];
				});
	});

	$('#shape').change(function(){
		var text = '{ "shape" : "' + $('#shape').val() + '" , "color" : "' + $('#color').val() +
		'" , "surface" : "' +$('#surface').val() + '" }' ;
		var image = document.getElementById('slika');
        $.ajax({
                type: 'POST',
				url: '/geometry',
				dataType: "json",
				data: text
				}).done(function(response) {
					image.src = response['image_path'];
				});
	});

	$('#edge').change(function(){
		var image = document.getElementById('slika');
		if(this.checked == true)
			$.ajax({
					type: 'POST',
					url: '/edge'
					}).done(function(response) {
						image.src = response['image_path'];
					});
		else
		image.src = "/static/pictures/original.jpg";
	});
});

	

