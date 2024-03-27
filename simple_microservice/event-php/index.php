<?php 
class ConnectionManager {

    public function getConnection() {
      $servername = 'database';
      $dbname = 'event';
      $username = 'root';
      $password = 'example';
      $port = 3306;
      $url  = "mysql:host=$servername;dbname=$dbname;port=$port";
  
      return new PDO($url, $username, $password);
    }
  
  }
$uri = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

switch ($method | $uri) {
   /*
   * Path: GET /api/users
   * Task: show all the users
   */
   case ($method == 'GET' && ($uri == '/event' || $uri == '/event/')):
        header('Content-Type: application/json');

        #step 1 : make PDO object
        $connMgr = new ConnectionManager();
        $pdo = $connMgr->getConnection(); #what is the method?

        #step 2 : prepare SQL statement
        $sql = "SELECT * FROM event where date > now()";  #need to remember the statements
        $stmt = $pdo->prepare($sql);

        #step 4: set the settings
        $stmt->setFetchMode(PDO::FETCH_ASSOC);
        $pdo->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_SILENT);

        #step 5 : execute
        $isOK= $stmt->execute();

        #step 6: retrieve result – only for GET/READ
        $result = [];
        while ($row = $stmt->fetch()) {
            $result[]= array_change_key_case( $row,  CASE_LOWER);
        }


        #step 7 : CLOSE connection
        $stmt = null;
        $pdo = null;

        #step 8 return result
        if (count($result) == 0){
            http_response_code(404);
            $result = ["code" => 404, "data"=> "Event not found."];

        } else {
            $result = ["code"=> 200, "data"=>$result];
        }

        echo json_encode($result, JSON_PRETTY_PRINT);
        break;

   /*
   * Path: GET /api/users/{id}
   * Task: get one user
   */
   case ($method == 'GET' && preg_match('/\/event\/[1-9]*/', $uri)):
        header('Content-Type: application/json');
        $id = basename($uri);

        #step 1 : make PDO object
        $connMgr = new ConnectionManager();
        $pdo = $connMgr->getConnection(); #what is the method?

        #step 2 : prepare SQL statement
        $sql = "SELECT * FROM event where eid = :id";  #need to remember the statements
        $stmt = $pdo->prepare($sql);

        $stmt->bindValue(":id",$id,PDO::PARAM_STR); 

        #step 4: set the settings
        $stmt->setFetchMode(PDO::FETCH_ASSOC);
        $pdo->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_SILENT);

        #step 5 : execute
        $isOK= $stmt->execute();

        #step 6: retrieve result – only for GET/READ
        $result =  $stmt->fetch();

        $result = array_change_key_case( $result,  CASE_LOWER);

        #step 7 : CLOSE connection
        $stmt = null;
        $pdo = null;

        #step 8 return result
        if ($result == false){
            http_response_code(404);
            $result = ["code" => 404, "data"=> "Event not found."];

        } else {
            $result = ["code"=> 200, "data"=>$result];
        }
        echo json_encode($result, JSON_PRETTY_PRINT);
        break;

   default:
       break;
}
?>