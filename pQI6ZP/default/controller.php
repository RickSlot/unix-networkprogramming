<?php 
$con=mysqli_connect("localhost","root","123","sniffer");
// Check connection
if (mysqli_connect_errno()) {
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM packets");
$only_once = true;
while($row = mysqli_fetch_array($result)) {
	echo "<tr>";
	foreach ($row as $value) {
		if ($only_once) {
			echo "<td>" . $value . "</td>";	
			$only_once = false;
		}else{
			$only_once = true;
		}
	}
	echo "</tr>";
}

mysqli_close($con);	