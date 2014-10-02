<?php 
// public function generate_table(){
	$con=mysqli_connect("localhost","root","123","sniffer");
// Check connection
	if (mysqli_connect_errno()) {
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}

	$result = mysqli_query($con,"SELECT * FROM packets WHERE timestamp >= " . $_GET['timestamp']);
	$timestamp = null;
	$data = "";
	while($row = mysqli_fetch_array($result)) {
		if($timestamp == null) {
			$timestamp = $row['timestamp'];
		}
		$data .= "<tr><td>";
		$data .= $row['dest_mac'] . "</td><td>" . $row['src_mac'] . "</td><td>" . $row['interface_protocol'] . "</td><td>" . $row['version'] . "</td><td>" . $row['ip_hdr_lngt'] . "</td><td>" . $row['ttl'] . "</td><td>" . $row['ip_protocol'] . "</td><td>" . $row['src_adress'] . "</td><td>" . $row['dest_adress'] . "</td><td>" . $row['src_port'] . "</td><td>" . $row['dest_port'] . "</td><td>" . $row['seq_num'] . "</td><td>" . $row['acknowledgement'] . "</td><td>" . $row['tcp_header_lngt'];
		$data .= "</td></tr>";
	}

	$json['timestamp'] = $timestamp;
	$json['data'] = $data;
	echo json_encode($json);

	mysqli_close($con);
// }