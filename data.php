<?php
//$output = system('python3.3 path/to/geedeekyuscript.py');
//echo $output;
$con=mysql_connect('','','');
mysql_select_db("", $con);
$result = mysql_query("SELECT A.dt as dt, A.total as total, B.dt as dt2, B.total as total2 FROM (SELECT @row_number1:=@row_number1+1 as RowNumber1, dt + INTERVAL 524190 MINUTE AS dt, total FROM Tgdq2015, (SELECT @row_number1:=0) AS x order by dt) AS A LEFT JOIN (SELECT @row_number2:=@row_number2+1 as RowNumber2, dt, total FROM Tgdq2016, (SELECT @row_number2:=0)AS y ORDER BY dt) AS B ON A.RowNumber1=B.RowNumber2");
//$r = mysql_fetch_array($result);
$rows = array();
while($r = mysql_fetch_object($result)) {
//      print_r(array($r));
        $rows[] = $r;
//      print_r($rows[0]);
}
//array_unshift($rows, date('Y/m/d H:i:s'));
$fp = fopen('gdq.json', 'w');
fwrite($fp, json_encode($rows, JSON_NUMERIC_CHECK));
fclose($fp);
//print json_encode($rows, JSON_NUMERIC_CHECK);
echo "it's done"
?>
