<?php
	$conn = new mysqli("localhost", "root", "pass123", "sign_language"); 
	//check connection 
	if(mysqli_connect_errno()){
	die("Connection error: " . mysqli_connect_error());
	}
	$sql_select = "SELECT road FROM result"; //执行SQL语句
    $result = mysqli_query($conn, $sql_select);
    while($row = $result->fetch_assoc()) {
    	$link = implode($row);
    }
    $conn->close();
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>A2S</title>
	<style>
		body {height: 100%; width: 99%; background-color: white;}
		div {height: 100%; width: 100%}
		video {width: 60%; margin-top: 15px; border-radius: 5px;}
		button {width: 10%; height: 40px; border: none; cursor: pointer; background-color: navajowhite; margin-top: 10px; border-radius: 10px;}
	</style>
</head>
<body>
	<!-- <h1><?php echo $link; ?></h1> -->
 	<div style="text-align:center"> 
		<video id="video" autoplay muted>
			<source src= <?php echo $link; ?> type="video/mp4">
		</video>
		<br>
		<button onclick="restart()">重看</button> 
	</div> 
	<script>
		var video = document.getElementById('video');
		function videoPlay(){
			video.play()
		}
		function restart(){
			video.currentTime=0;
			setTimeout(videoPlay(), 100);
		}
	</script>
</body>
</html>
