<?php
echo "<h1>Covid Cases</h1>\n";
chdir('charts');
foreach (glob('*_small.png') as $c=>$i) {
	echo "<h2>".($c+1).": ".
	str_replace("_small.png","",$i)
	."</h2><a href=\"charts/".
	str_replace("_small","_300dpi",$i)
	."\"><img src=\"charts/$i\" alt=\"$i\"></a><br>\n";
}
echo "<a href=\"https://github.com/dk5ee/covidcharts\">https://github.com/dk5ee/covidcharts</a>";