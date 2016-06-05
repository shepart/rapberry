<?php
include_once 'config.inc.php';

header('Content-Type: application/json');

class Temperatur {
        var $date;
        var $sensor
        var $temperatur

        function getDate(){
                return $this->date;
        }

        function getSensor(){
                return $this->sensor;
        }

        function getTemp(){
                return $this->temp;
        }

        static function  getClass() {
                return __CLASS__;
        }
}

$db = new PDO('mysql:host='.$config['db']['host'].';dbname='.$config['db']['name'].';charset=utf8mb4', $config['db']['user'], $config['db']['password']);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

try {
        //connect as appropriate as above
        $stmt = $db->query("SELECT DATE(Datum) as 'date', sensor_id as 'sensor', temperatur as 'temp' FROM statistik.temp WHERE datediff(NOW(), Datum) < 9 GROUP BY DAY(Datum), MONTH(Datum), YEAR(Datum) ORDER BY date");
        $tempDaten = $stmt->fetchAll(PDO::FETCH_CLASS, Temperatur::getClass());

        if($config['debug']){
                print_r($tempDaten);
        }

        $tempDaten[$i]->getSensor();
        }

        if($config['debug']){
                print_r($tempDaten);
                print_r(array_slice($tempDaten, 1));
        }

        echo json_encode(array_slice($tempDaten, 1));

} catch(PDOException $ex) {
        echo "An Error occured!"; //user friendly message
        echo ($ex->getMessage());
