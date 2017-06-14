<?php
require_once 'sml_parser.php';

$dbconfig['host'] = "localhost";
$dbconfig['user'] = "root";
$dbconfig['password'] = "123456";
$dbconfig['db'] = "statistik";

$pathname=__DIR__.'/data/';
print_r ($pathname);
if ($handle = opendir($pathname)) {
    while (false !== ($file = readdir($handle))) {
        if ($file != "." && $file != "..") {
            $files[]=$file;
        }
    }

    if(is_array($files)) {
        sort($files);

        foreach($files as $file) {
            if(substr($file,0,9)=='serialin_') {
                $sml_parser = new SML_PARSER();
                $sml_parser->parse_sml_file($pathname.$file);
                $values = $sml_parser->get_first_values();
                
#                print_r($values);
                
                $time = date('Y-m-d H:i:s',filemtime($pathname.$file));

                $OBIS_1_8_1 = $values['0100010801FF']['value']*$values['0100010801FF']['scaler']/1000; # Wh -> kWh
                $public_key = $values['8181C78205FF']['value'];
                $active_power = $values['0100100700FF']['value'];

                $mysqli = new mysqli();
                
                $connection = $mysqli->connect($dbconfig['host'],   $dbconfig['user'], $dbconfig['password'], $dbconfig['db']);
                
                $sql = "INSERT INTO stromzaehler
                        (timestamp,public_key,zaehlerstand,active_power)
                        VALUES ('$time','$public_key','$OBIS_1_8_1','$active_power')";
        $mysqli->query($sql) or die($sql);
        
        
        //Trägt einen Snapshot der aktuellen Daten in eine extra Tabelle ein
        //damit der Raspi nicht immer durch die komplette Tabelle pflügen muss
        $sql = "UPDATE strom_snapshot SET zeitstempel=CURRENT_TIMESTAMP, zaehlerstand='$OBIS_1_8_1', wirkleistung='$active_power'";
         $mysqli->query($sql) or die($sql);
		echo $pathname . "\n";
                unlink($pathname.($file));
            }
        }
    }
    closedir($handle);
}
?>
