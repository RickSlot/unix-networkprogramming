<?php 
$con=mysqli_connect("localhost","unix","123","sniffer");
// Check connection
if (mysqli_connect_errno()) {
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
// print_r($_POST);
// die();
$resulttcp = mysqli_query($con,"SELECT * FROM packets WHERE `id` > " . $_POST['id'] . " ORDER BY id DESC LIMIT 50");//LIMIT 50
$resultudp = mysqli_query($con,"SELECT * FROM packetsudp WHERE `id` > " . $_POST['id'] . " ORDER BY id DESC LIMIT 50");//LIMIT 50
$idTcp = null;
$idUdp = null;
$datatcp = "";
$dataudp = "";
$only_once = true;

while($row = mysqli_fetch_array($resulttcp)) {
	if($idTcp == null) {
		$idTcp = $row['id'];
	}

	$datatcp .= "<tr>";
	foreach ($row as $value) {
		if ($only_once) {
			$datatcp .= "<td>" . $value . "</td>";	
			$only_once = false;
		}else{
			$only_once = true;
		}
	}
	$datatcp .= "</tr>";
}

while($row = mysqli_fetch_array($resultudp)) {
	if($idUdp == null) {
		$idUdp = $row['id'];
	}

	$dataudp .= "<tr>";
	foreach ($row as $value) {
		if ($only_once) {
			$dataudp .= "<td>" . $value . "</td>";	
			$only_once = false;
		}else{
			$only_once = true;
		}
	}
	$dataudp .= "</tr>";
}


$json = array();
$json['idTcp'] = $idTcp;
$json['idUdp'] = $idUdp;
$json['datatcp'] = $datatcp;
$json['dataudp'] = $dataudp;
echo json_encode($json);

mysqli_close($con);
