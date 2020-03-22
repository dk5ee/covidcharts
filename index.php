<?php
echo "<h1>Covid Cases</h1>\n";

if(file_exists('lastupdate.txt')) {
    echo "last update: " . date ("r", filemtime('lastupdate.txt'));
}

foreach (array(
            'charts'=>'Johns Hopkins University', 
            'who'=>'World Health Organisation',
            'ecdc'=>'European Centre for Disease Prevention and Control')
        as $directory=>$description) {
    chdir($directory);
    echo "<div style=\"float;left\"><h2>Data from $description</h2>\n";
    foreach (glob('*_small.png') as $c=>$i) {
	    echo "<h3>".($c+1).":</h3> ".
    	str_replace("_small.png","",$i)
	    ."<a href=\"$directory/".
    	str_replace("_small","_300dpi",$i)
	    ."\"><img src=\"$directory/$i\" alt=\"$i\"></a><br>
        <a href=\"$directory/".str_replace("_small.png",".csv",$i)."\">csvfile</a><br>\n";
    }
    echo "</div>\n";
    chdir('..');
}
echo "<a href=\"https://github.com/dk5ee/covidcharts\">https://github.com/dk5ee/covidcharts</a>";
?>
<a href="https://bedah.de/bedah.php">by bedah</a>


