<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Document</title>
		<link rel="stylesheet" href="/bower_components/bootstrap/dist/css/bootstrap.css">
		<link rel="stylesheet" href="/bower_components/fontawesome/css/font-awesome.min.css">
		<script type="text/javascript" src="/bower_components/jquery/dist/jquery.min.js"></script>
		<script type="text/javascript" src="/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
	</head>
	<body>
		<div class="container">
			<div class="row">
				<div class="col-lg-12">
					<table class="table table-no-border table-hover">
					<thead>
						<tr>
							<th>
								<span>Destination MAC</span>
							</th>
							<th>
								<span>Source MAC</span>
							</th>
							<th>
								<span>Interface Protocol</span>
							</th>
							<th>
								<span>Version</span>
							</th>
							<th>
								<span>IP Header Length</span>
							</th>
							<th>
								<span>TTL</span>
							</th>
							<th>
								<span>IP Protocol</span>
							</th>
							<th>
								<span>Source Address</span>
							</th>
							<th>
								<span>Destination Address</span>
							</th>
							<th>
								<span>Source Port</span>
							</th>
							<th>
								<span>Destination Port</span>
							</th>
							<th>
								<span>Sequence Number</span>
							</th>
							<th>
								<span>Acknowledgement</span>
							</th>
							<th>
								<span>TCP Header Length</span>
							</th>
							<th>
								<span>TimeStamp</span>
							</th>
						</tr>
						</thead>
						<tbody><?php include 'controller.php'; ?></tbody>
					</table>
				</div>
			</div>
		</div>
	</body>
</html>