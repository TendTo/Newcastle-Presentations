<html>
 <head>
  <title>Hello, is it me you are looking for?</title>

  <meta charset="utf-8"> 

  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

</head>
<body>
    <div class="container">
    <h1>Users!</h1>
    <table class="table table-striped">
    <thead><tr><th></th><th>id</th><th>name</th></tr></thead>
<?php
    $conn = new mysqli('db', 'user', 'test', 'myDb');
    $query = 'SELECT * From Person';
    $result = $conn->query($query);
    while($value = $result->fetch_assoc()){
        echo '<tr>';
        echo '<td><a href="#"><span class="glyphicon glyphicon-search"></span></a></td>';
        foreach($value as $element){
            echo '<td>' . $element . '</td>';
        }

        echo '</tr>';
    }
    echo '</table>';

    $result->close();

    mysqli_close($conn);
?>
    </div>
</body>
</html>
