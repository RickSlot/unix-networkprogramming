<?php 
$con=mysqli_connect("localhost","root","123","sniffer");
// Check connection
if (mysqli_connect_errno()) {
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
// print_r($_POST);
// die();
$result = mysqli_query($con,"SELECT * FROM packets WHERE `id` >= " . $_POST['id'] . " ORDER BY id DESC LIMIT 50");//LIMIT 50
$id = null;
$data = "";
$only_once = true;
while($row = mysqli_fetch_array($result)) {
	if($id == null) {
		$id = $row['id'];
	}

	$data .= "<tr>";
	foreach ($row as $value) {
		if ($only_once) {
			$data .= "<td>" . $value . "</td>";	
			$only_once = false;
		}else{
			$only_once = true;
		}
	}
	$data .= "</tr>";
}
$json = array();
$json['id'] = $id;
$json['data'] = $data;
echo json_encode($json);

mysqli_close($con);