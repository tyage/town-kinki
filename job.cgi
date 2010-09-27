#!/usr/bin/perl

require 'town_ini.cgi';
require 'town_lib.pl';
&decode;

if($in{'mode'} eq "make"){&make;}
elsif($in{'mode'} eq "top"){&top;}
else{&error("不正進入か？");}

exit;

sub top{
	@job_data=&readfile("log_dir/joblog.cgi");
	foreach(@job_data){
    	($toukousya,$job_name,$job_kokugo,$job_suugaku,$job_rika,$job_syakai,$job_eigo,$job_ongaku,$job_bijutu,$job_BMI_min,$job_BMI_max,$job_looks,$job_tairyoku,$job_kenkou,$job_speed,$job_power,$job_wanryoku,$job_kyakuryoku,$job_kyuuyo,$job_siharai,$job_love,$job_unique,$job_etti,$job_sex,$job_sintyou,$job_energy,$job_nou_energy,$job_rank,$job_syurui,$job_bonus,$job_syoukyuuritu)= split(/<>/);
    	
		if ($job_BMI_min eq "" && $job_BMI_max eq ""){$BMI_hani = "";}
		elsif ($job_BMI_min eq "" ){$BMI_hani = "$job_BMI_max以下";}
		elsif ($job_BMI_max eq "" ){$BMI_hani = "$job_BMI_min以上";}
		else {$BMI_hani = "$job_BMI_min～$job_BMI_max";}
		if ($job_siharai eq "1"){$sihrai_seikei = "日払い";}
		else{$sihrai_seikei = "$job_siharai回出勤ごと";}
		if ($job_sintyou){$job_sintyou = "$job_sintyou以上";}
		if($job_sex eq "m") {$job_sex = "男";}
		elsif($job_sex eq "f"){$job_sex = "女";}
		
		$comment .= <<"EOM";
		<tr bgcolor=#ffcc66 align=center onmouseover="Navi('$img_dir/depart.gif', 'デパート', '<table border=1><tr><td>国語：$job_kokugo</td><td>数学：$job_suugaku</td><td>理科：$job_rika</td><td>社会：$job_syakai</td><td>英語：$job_eigo</td><td>音楽：$job_ongaku</td><td>美術：$job_bijutu</td></tr><tr><td>ルックス：$job_looks</td><td>体力：$job_tairyoku</td><td>健康：$job_kenkou</td><td>スピード：$job_speed</td><td>パワー：$job_power</td><td>腕力：$job_wanryoku</td><td>脚力：$job_kyakuryoku</td></tr><tr><td>LOVE：$job_love</td><td>面白さ：$job_unique</td><td>エッチ：$job_etti</td></tr></table>');"><td nowrap>$job_name</td><td nowrap>$BMI_hani</td><td>$job_sex</td><td nowrap>$job_sintyou</td><td align=right nowrap>$job_kyuuyo円</td><td nowrap>×$job_bonus</td><td nowrap>$sihrai_seikei</td><td>$job_energy</td><td>$job_nou_energy</td></tr>
EOM
	}

	&header(syokudou_style);
	print <<"EOM";
	<form action="job.cgi" method="POST">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>make<>">
	名前：<input type="text" name="job_name" size="6">
	国語：<input type="text" name="job_kokugo" size="6">
	<input type="text" name="job_suugaku" size="6">
	<input type="text" name="job_rika" size="6">
	<input type="text" name="job_syakai" size="6">
	<input type="text" name="job_eigo" size="6">
	<input type="text" name="job_ongaku" size="6">
	<input type="text" name="job_bijutu" size="6">
	<input type="text" name="job_BMI_min" size="6">
	<input type="text" name="job_BMI_max" size="6">
	<input type="text" name="job_looks" size="6">
	<input type="text" name="job_tairyoku" size="6">
	<input type="text" name="job_kenkou" size="6">
	<input type="text" name="job_speed" size="6">
	<input type="text" name="job_power" size="6">
	<input type="text" name="job_wanryoku" size="6">
	<input type="text" name="job_kyakuryoku" size="6">
	<input type="text" name="job_kyuuyo" size="6">
	<input type="text" name="job_siharai" size="6">
	<input type="text" name="job_love" size="6">
	<input type="text" name="job_unique" size="6">
	<input type="text" name="job_etti" size="6">
	<input type="text" name="job_sex" size="6">
	<input type="text" name="job_sintyou" size="6">
	<input type="text" name="job_energy" size="6">
	<input type="text" name="job_nou_energy" size="6">
	<input type="text" name="job_rank" size="6">
	<input type="text" name="job_syurui" size="6">
	<input type="text" name="job_bonus" size="6">
	<input type="text" name="job_syoukyuuritu" size="6">
	<input type="submit" value="投稿する">
	</form>
	<table width="95%" border="0" cellspacing="1" cellpadding="4" align=center class=yosumi>
	<tr><td colspan=25><font color=#336699>凡例：(国)＝国語、(数)＝数学、(理)＝理科、(社)＝社会、(英)＝英語、(音)＝音楽、(美)＝美術、(ル)＝ルックス、(体)＝体力、(健)＝健康、(ス)＝スピード、(パ)＝パワー、(腕)＝腕力、(脚)＝脚力、(H)＝エッチ</font></td></tr>
	<tr bgcolor=#ff9933 align=center><td nowrap rowspan=2>職業</td><td align=center colspan=3>条　件</td><td rowspan=2 align=center>給　料<br>（1回出勤）</td><td rowspan=2 align=center>ボーナス</td><td rowspan=2>支払い</td><td rowspan=2 nowrap>身体<br>消費</td><td rowspan=2 nowrap>頭脳<br>消費</td></tr>
	<tr bgcolor=#ffcc33 align=center><td nowrap>体格指数</td><td nowrap>性別</td><td nowrap>身長</td></tr>
	$comment
	</table>
EOM

exit;
}

sub make{
$a=$in{'job_kokugo'}.$in{'job_suugsku'}.$in{'job_rika'}.$in{'job_syakai'}.$in{'job_eigo'}.$in{'job_ongaku'}.$in{'job_bijutu'}.$in{'job_BMI_min'}.$in{'job_BMI_max'}.$in{'job_looks'}.$in{'job_tairyoku'}.$in{'job_kenkou'}.$in{'job_speed'}.$in{'job_power'}.$in{'job_wanryoku'}.$in{'job_kyakuryoku'}.$in{'job_kyuuyo'}.$in{'job_siharai'}.$in{'job_love'}.$in{'job_unique'}.$in{'job_etti'}.$in{'job_sintyou'}.$in{'job_energy'}.$in{'job_nou_energy'}.$in{'job_rank'}.$in{'job_syurui'}.$in{'job_bonus'}.$in{'job_syoukyuuritu'};
$b=$a*2;
	if($a =~ /[^0-9]/){&error("金額は半角数字で記入してください$b");}

	@job_data=&readfile("log_dir/joblog.cgi");
	unshift (@job_data,"$in{'name'}<>$in{'job_name'}<>$in{'job_kokugo'}<>$in{'job_suugaku'}<>$in{'job_rika'}<>$in{'job_syakai'}<>$in{'job_eigo'}<>$in{'job_ongaku'}<>$in{'job_bijutu'}<>$in{'job_BMI_min'}<>$in{'job_BMI_max'}<>$in{'job_looks'}<>$in{'job_tairyoku'}<>$in{'job_kenkou'}<>$in{'job_speed'}<>$in{'job_power'}<>$in{'job_wanryoku'}<>$in{'job_kyakuryoku'}<>$in{'job_kyuuyo'}<>$in{'job_siharai'}<>$in{'job_love'}<>$in{'job_unique'}<>$in{'job_etti'}<>$in{'job_sex'}<>$in{'job_sintyou'}<>$in{'job_energy'}<>$in{'job_nou_energy'}<>$in{'job_rank'}<>$in{'job_syurui'}<>$in{'job_bonus'}<>$in{'job_syoukyuuritu'}<>\n");
	&writefile("log_dir/joblog.cgi",@job_data);
	
	&header(syokudou_style);
	print <<"EOM";
	
EOM

exit;
}