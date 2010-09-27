#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
# メルマガ受け取りで「合言葉」を入れて一致すると良いことが一回行われる。
#　 Edit:たっちゃん　2007/11/12
#################################
# 参加済みファイル　新しいイベントの時は空にする。
$sankazumi = "./log_dir/tokuten_log.cgi";
#######################################
# unit.pl
#"特典" => "<form method=POST action=\"tokuten.cgi\"><input type=hidden name=mode value=\"tokuten\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/kentiku_yotei.gif'  onMouseOver='onMes5(\"特典\")' onMouseOut='onMes5(\"\")'></td></form>\n",
#######################################
#	print <<"EOM";
#<form method=POST action="tokuten.cgi">
#<input type=hidden name=mode value="tokuten">
#<input type=hidden name=name value="$name">
#<input type=hidden name=pass value="$pass">
#<input type=hidden name=k_id value="$k_id">
#<input type=hidden name=town_no value="$in{'town_no'}">
#<input type=submit value="特典">
#</form>
#EOM
#######################################

# アイテム渡しのファイル
$aitem_fail = './dat_dir/syouhin.cgi';
#######################################

$this_script = "tokuten.cgi";
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。");}

#条件分岐

	if($in{'mode'} eq "tokuten"){&tokuten;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub tokuten {
	open(MA,"< $sankazumi") || &error("$sankazumiが開けません");
	eval{ flock (MK,1); };
	$kanri = <MA>;
	@sankasya = <MA>;
	close(MA);
	($nanba0,$nanba1,$aikotba1,$aikotoba2,$s_tim0,$s_sec0,$s_min0,$s_hour0,$s_day0,$s_mon0,$s_year0,$e_tim0,$e_sec0,$e_min0,$e_hour0,$e_day0,$e_mon0,$e_year0,$s_tim1,$s_sec1,$s_min1,$s_hour1,$s_day1,$s_mon1,$s_year1,$e_tim1,$e_sec1,$e_min1,$e_hour1,$e_day1,$e_mon1,$e_year1,$bunrui,$bunrui1,$atai,$atai1,$sybetu,$sybetu1,$syouhin,$syouhin1) = split(/<>/,$kanri);

	if ($in{'command'} eq 'kakikae1'){
		if($nanba0 eq ''){$nanba0 = 1;$nanba1 = 2;}

		$aikotba1 = $in{'aikotba1'};
		$aikotoba2 = $in{'aikotoba2'};

		$s_year0 = $in{'s_year0'};
		if($s_year0 =~ /\D/){$mesegi .= "半角数字を入れてください。年 1<br>\n";}
		$s_mon0 = $in{'s_mon0'};
		if($s_mon0 < 1 || $s_mon0 > 12 || $s_mon0 =~ /\D/){$mesegi .= "半角数字を入れてください。月 1<br>\n";}
		$s_day0 = $in{'s_day0'};
		if($s_day0 < 1 || $s_day0 > 31 || $s_day0 =~ /\D/){$mesegi .= "半角数字を入れてください。日 1<br>\n";}
		$s_hour0 = $in{'s_hour0'};
		if($s_hour0 < 0 || $s_hour0 > 23 || $s_hour0 =~ /\D/){$mesegi .= "半角数字を入れてください。時 <br>\n";}
		$s_min0 = $in{'s_min0'};
		if($s_min0 < 0 || $s_min0 > 59 || $s_min0 =~ /\D/){$mesegi .= "半角数字を入れてください。分 1<br>\n";}
		$s_sec0 = $in{'s_sec0'};
		if($s_sec0 < 0 || $s_sec0 > 59 || $s_sec0 =~ /\D/){$mesegi .= "半角数字を入れてください。秒 1<br>\n";}

		$e_year0 = $in{'e_year0'};
		if($e_year0 =~ /\D/){$mesegi .= "半角数字を入れてください。年 2";}
		$e_mon0 = $in{'e_mon0'};
		if($e_mon0 < 1 || $e_mon0 > 12 || $e_mon0 =~ /\D/){$mesegi .= "半角数字を入れてください。月 2<br>\n";}
		$e_day0 = $in{'e_day0'};
		if($e_day0 < 1 || $e_day0 > 31 || $e_day0 =~ /\D/){$mesegi .= "半角数字を入れてください。日 2<br>\n";}
		$e_hour0 = $in{'e_hour0'};
		if($e_hour0 < 0 || $e_hour0 > 23 || $e_hour0 =~ /\D/){$mesegi .= "半角数字を入れてください。時 2<br>\n";}
		$e_min0 = $in{'e_min0'};
		if($e_min0 < 0 || $e_min0 > 59 || $e_min0 =~ /\D/){$mesegi .= "半角数字を入れてください。分 2<br>\n";}
		$e_sec0 = $in{'e_sec0'};
		if($e_sec0 < 0 || $e_sec0 > 59 || $e_sec0 =~ /\D/){$mesegi .= "半角数字を入れてください。秒 2<br>\n";}

		$s_year1 = $in{'s_year1'};
		if($s_year1 =~ /\D/){$mesegi .= "半角数字を入れてください。年 3<br>\n";}
		$s_mon1 = $in{'s_mon1'};
		if($s_mon1 < 1 || $s_mon0 > 12 || $s_mon0 =~ /\D/){$mesegi .= "半角数字を入れてください。月 3<br>\n";}
		$s_day1 = $in{'s_day1'};
		if($s_day1 < 1 || $s_day0 > 31 || $s_day0 =~ /\D/){$mesegi .= "半角数字を入れてください。日 3<br>\n";}
		$s_hour1 = $in{'s_hour1'};
		if($s_hour1 < 0 || $s_hour0 > 23 || $s_hour0 =~ /\D/){$mesegi .= "半角数字を入れてください。時 3<br>\n";}
		$s_min1 = $in{'s_min1'};
		if($s_min1 < 0 || $s_min0 > 59 || $s_min0 =~ /\D/){$mesegi .= "半角数字を入れてください。分 3<br>\n";}
		$s_sec1 = $in{'s_sec1'};
		if($s_sec1 < 0 || $s_sec0 > 59 || $s_sec0 =~ /\D/){$mesegi .= "半角数字を入れてください。秒 3<br>\n";}

		$e_year1 = $in{'e_year1'};
		if($e_year1 =~ /\D/){$mesegi .= "半角数字を入れてください。年 4<br>\n";}
		$e_mon1 = $in{'e_mon1'};
		if($e_mon1 < 1 || $e_mon1 > 12 || $e_mon1 =~ /\D/){$mesegi .= "半角数字を入れてください。月 4<br>\n";}
		$e_day1 = $in{'e_day1'};
		if($e_day1 < 1 || $e_day1 > 31 || $e_day1 =~ /\D/){$mesegi .= "半角数字を入れてください。日 4<br>\n";}
		$e_hour1 = $in{'e_hour1'};
		if($e_hour1 < 0 || $e_hour1 > 23 || $e_hour1 =~ /\D/){$mesegi .= "半角数字を入れてください。時 4<br>\n";}
		$e_min1 = $in{'e_min1'};
		if($e_min1 < 0 || $e_min1 > 59 || $e_min1 =~ /\D/){$mesegi .= "半角数字を入れてください。分 4<br>\n";}
		$e_sec1 = $in{'e_sec1'};
		if($e_sec1 < 0 || $e_sec1 > 59 || $e_sec1 =~ /\D/){$mesegi .= "半角数字を入れてください。秒 4<br>\n";}

		$bunrui = $in{'bunrui'};
		$atai = $in{'atai'};if($atai =~ /\D/){$mesegi .= "半角数字を入れてください。お金<br>\n";}
		$sybetu = $in{'sybetu'};
		$syouhin = $in{'syouhin'};

		$bunrui1 = $in{'bunrui1'};
		$atai1 = $in{'atai1'};if($atai =~ /\D/){$mesegi .= "半角数字を入れてください。お金<br>\n";}
		$sybetu1 = $in{'sybetu1'};
		$syouhin1 = $in{'syouhin1'};

		$kanri = "$nanba0<>$nanba1<>$aikotba1<>$aikotoba2<>$s_tim0<>$s_sec0<>$s_min0<>$s_hour0<>$s_day0<>$s_mon0<>$s_year0<>$e_tim0<>$e_sec0<>$e_min0<>$e_hour0<>$e_day0<>$e_mon0<>$e_year0<>$s_tim1<>$s_sec1<>$s_min1<>$s_hour1<>$s_day1<>$s_mon1<>$s_year1<>$e_tim1<>$e_sec1<>$e_min1<>$e_hour1<>$e_day1<>$e_mon1<>$e_year1<>$bunrui<>$bunrui1<>$atai<>$atai1<>$sybetu<>$sybetu1<>$syouhin<>$syouhin1<>\n";

		open(MA,"> $sankazumi") || &error("$sankazumiが開けません");
		eval{ flock (MA, 2); };
		print MA $kanri;
		print MA @sankasya;
		close(MA);
	}
	use Time::Local;
	eval{ $s_tim0 = timelocal($s_sec0, $s_min0, $s_hour0, $s_day0, $s_mon0-1, $s_year0); };
	($s_sec,$s_min,$s_hour,$s_day,$s_mon,$s_year) = localtime($s_tim0);
	$deit0 = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$s_year+1900,$s_mon+1,$s_day,$s_hour,$s_min,$s_sec);

	eval{ $e_tim0 = timelocal($e_sec0, $e_min0, $e_hour0, $e_day0, $e_mon0-1, $e_year0); };
	($e_sec,$e_min,$e_hour,$e_day,$e_mon,$e_year) = localtime($e_tim0);
	$deit1 = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$e_year+1900,$e_mon+1,$e_day,$e_hour,$e_min,$e_sec);

	if ($s_tim0 >= $e_tim0){$mesegi = "開始日時($deit0)か終了日時($deit1)にミスがあります。1<br>\n";}

	eval{ $s_tim1 = timelocal($s_sec1, $s_min1, $s_hour1, $s_day1, $s_mon1 -1, $s_year1); };
	($s_sec,$s_min,$s_hour,$s_day,$s_mon,$s_year) = localtime($s_tim1);
	$deit2 = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$s_year+1900,$s_mon+1,$s_day,$s_hour,$s_min,$s_sec);

	eval{ $e_tim1 = timelocal($e_sec1, $e_min1, $e_hour1, $e_day1, $e_mon1 -1, $e_year1); };
	($e_sec,$e_min,$e_hour,$e_day,$e_mon,$e_year) = localtime($e_tim1);
	$deit3 = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$e_year+1900,$e_mon+1,$e_day,$e_hour,$e_min,$e_sec);

	if ($s_tim1 >= $e_tim1){$mesegi .= "開始日時($deit2)か終了日時($deit3)にミスがあります。2<br>\n";}

	if ($s_tim1 && $e_tim0 >= $s_tim1){$mesegi .= "第一終了日時($deit1)か第二開始日時($deit2)にミスがあります。3<br>\n";}

	$ima_time = time;
	if (!$e_tim0){
		$mesegi2 = "イベントは行われていません。<br>\n";
	}elsif($s_tim0 >= $ima_time){
		$mesegi2 = "イベントは、$deit0 より、$deit1 の間行われます。<br>\n";
	}elsif($s_tim0 < $ima_time && $e_tim0 > $ima_time){
		$mesegi2 = "イベントは、開催中、$deit1 に終わります。<br>\n";
		$eventon_f = 1;
		if($koushin){$koushin = 0;}
	}else{
		$mesegi2 = "イベントは終了しました。<br>\n";
	}

	if($e_tim0 < $ima_time && !$koushin && $e_tim1){
		foreach (@sankasya){
			($kaime,$t_name,$datim,$t_ima_time) = split(/<>/);
			if($nanba0 > $kaime){next;}
			push @new_sakasya,"$kaime<>$t_name<>$datim<>$t_ima_time<>\n";
		}
		@sankasya = (@new_sakasya);

		$aikotba1 = $aikotba2;$aikotba2="";

		$nanba0 = $nanba1;$nanba1++;
		$aikotba1 = $aikotoba2;$aikotoba2 = "";

		$s_tim0 = $s_tim1;$s_tim1 = 0;
		$s_sec0 = $s_sec1;$s_sec1 = '';
		$s_min0 = $s_min1;$s_min1 = '';
		$s_hour0 = $s_hour1;$s_hour1 = '';
		$s_day0 = $s_day1;$s_day1 = '';
		$s_mon0 = $s_mon1;$s_mon1 = '';
		$s_year0 = $s_year1;$s_year1 = '';

		$e_tim0 = $e_tim1;$e_tim1 = 0;
		$e_sec0 = $e_sec1;$e_sec1 = '';
		$e_min0 = $e_min1;$e_min1 = '';
		$e_hour0 = $e_hour1;$e_hour1 = '';
		$e_day0 = $e_day1;$e_day1 = '';
		$e_mon0 = $e_mon1;$e_mon1 = '';
		$e_year0 = $e_year1;$e_year1 = '';


		$bunrui = $bunrui1;$bunrui1 = "";
		$atai = $atai1;$atai1 = "";
		$sybetu = $sybetu1;$sybetu1 = "";
		$syouhin = $syouhin1;$syouhin1 = "";

		$kanri = "$nanba0<>$nanba1<>$aikotba1<>$aikotoba2<>$s_tim0<>$s_sec0<>$s_min0<>$s_hour0<>$s_day0<>$s_mon0<>$s_year0<>$e_tim0<>$e_sec0<>$e_min0<>$e_hour0<>$e_day0<>$e_mon0<>$e_year0<>$s_tim1<>$s_sec1<>$s_min1<>$s_hour1<>$s_day1<>$s_mon1<>$s_year1<>$e_tim1<>$e_sec1<>$e_min1<>$e_hour1<>$e_day1<>$e_mon1<>$e_year1<>$bunrui<>$bunrui1<>$atai<>$atai1<>$sybetu<>$sybetu1<>$syouhin<>$syouhin1<>\n";

		open(MA,"> $sankazumi") || &error("$sankazumiが開けません");
		eval{ flock (MA, 2); };
		print MA $kanri;
		print MA @sankasya;
		close(MA);

		$koushin = 1;
	}

	foreach (@sankasya){
		($kaime,$fuku_name,$nichiji,$hinithi) = split(/<>/);
		if ($in{'name'} eq $fuku_name && $nanba0 == $kaime){
			$mesegi4 = "期間中一度しか参加できません。<br>次回の参加をお待ちしています。<br>\n";
			$sankaari = 1;
		}
	}
	open(OUT,"< $aitem_fail") || &error("Open Error : $aitem_fail");
	eval{ flock (OUT, 1); };
	$tempo = <OUT>;
	@item_list0 = <OUT>;
	close(OUT);

	if($eventon_f && !$sankaari && $in{'aikotoba'} eq $aikotba1){
		$monokiroku_file="./member/$k_id/mono.cgi";
		open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
		eval{ flock (OUT, 1); };
		@my_item_list = <OUT>;
		close(OUT);

		if($bunrui eq 'item'){

			$motikazu = 0;
			foreach (@my_item_list){
				&syouhin_sprit($_);
				if ($syo_syubetu eq 'ギフト' || $syo_syubetu eq 'ギフト商品' || $syo_taikyuu <= 0){next;}
				$motikazu++;
			}
			if ($motikazu >= $syoyuu_gendosuu){&error("持ち物が上限だったので、諦めた。$motikazu/$syoyuu_gendosuu");}

			if($sankaari != 1){

				$i = 0;
				foreach (@item_list0){
					&syouhin_sprit($_);
					if($syo_syubetu eq $sybetu && $syo_hinmoku eq $syouhin){
						$point_basyo = $i;
						$item_attayo = 1;
						last;
					}
					$i++;
				}

				&syouhin_sprit($item_list0[$point_basyo]);
				$syo_kounyuubi = $ima_time;
				&syouhin_temp;
				push @my_item_list,$syo_temp;

				if($item_attayo){
					open(OUT,"> $monokiroku_file") || &error("Open Error : $monokiroku_file");
					eval{ flock (OUT, 2); };
					print OUT @my_item_list;
					close(OUT);
					$mesegi3 = "$sybetu の $syouhin をもらいました。";
				}else{
					$mesegi3 = "アイテムをもらえなかった。";
				}
			}
		}
		if($bunrui eq 'okane'){
			$money += $atai;
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			$mesegi3 = "$atai 円もらいました。";
		}

		$kaime = $nanba0;

		(@imatime0) = localtime($ima_time);
		$deit4 = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$imatime0[5]+1900,$imatime0[4]+1,$imatime0[3],$imatime0[2],$imatime0[1],$imatime0[0]);
		unshift @sankasya,"$kaime<>$in{'name'}<>$deit4<>$ima_time<>\n";

		open(MA,"> $sankazumi") || &error("$sankazumiが開けません");
		eval{ flock (MA, 2); };
		print MA $kanri;
		print MA @sankasya;
		close(MA);
	
	}elsif($in{'aikotoba'} && !$sankaari){
		$mesegi3 = "合い言葉が違っています。<br>\n";
	}else{
		$mesegi3 = "";
	}

	if($bunrui eq "item"){
		$bunluidisp ="<select name=bunrui><option value=\"item\" selected>アイテム</option><option value=\"okane\">お金</option></select>"
	}else{
		$bunluidisp ="<select name=bunrui><option value=\"item\">アイテム</option><option value=\"okane\" selected>お金</option></select>"
	}
	if($bunrui1 eq "item"){
		$bunluidisp1 ="<select name=bunrui1><option value=\"item\" selected>アイテム</option><option value=\"okane\">お金</option></select>"
	}else{
		$bunluidisp1 ="<select name=bunrui1><option value=\"item\">アイテム</option><option value=\"okane\" selected>お金</option></select>"
	}

	&header(ginkou_style);
	if($in{'name'} eq $admin_name && $in{'command'} eq 'kakikae'){

		if($sybetu && $syouhin){
			foreach (@item_list0){
				&syouhin_sprit($_);
				if($syo_syubetu eq $sybetu && $syo_hinmoku eq $syouhin){
					$item_attayo0 = "ありました。";
					last;
				}
			}
		}
		if($sybetu1 && $syouhin1){
			foreach (@item_list0){
				&syouhin_sprit($_);
				if($syo_syubetu eq $sybetu1 && $syo_hinmoku eq $syouhin1){
					$item_attayo1 = "ありました。";
					last;
				}
			}
		}
		if(!$item_attayo0){$item_attayo0 = "ありませんでした。";}
		if(!$item_attayo1){$item_attayo1 = "ありませんでした。";}

		print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<TR><TD align=center>
<div class=purasu align=center>＋＋＋管理者設定入力＋＋＋</div>
<table border=0 bgcolor=#ffffff cellspacing=0 cellpadding=3 align=center width=$wid><tr><td>
$mesegi
$mesegi2
$mesegi3
$mesegi4
</td></tr>
<tr><td>
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="tokuten">
<input type=hidden name=command value="kakikae1">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
スタート1 合言葉
<input type=text name=aikotba1 value="$aikotba1" maxlength="10">
<input type=text name=s_year0 size=5 value="$s_year0" maxlength="4">年
<input type=text name=s_mon0 size=3 value="$s_mon0" maxlength="2">月
<input type=text name=s_day0 size=3 value="$s_day0" maxlength="2">日
<input type=text name=s_hour0 size=3 value="$s_hour0" maxlength="2">時
<input type=text name=s_min0 size=3 value="$s_min0" maxlength="2">分
<input type=text name=s_sec0 size=3 value="$s_sec0" maxlength="2">秒
分類 $bunluidisp
<input type=text name=atai value="$atai" maxlength="10">円　または　
<input type=text name=sybetu value="$sybetu" maxlength="10">の
<input type=text name=syouhin value="$syouhin" maxlength="20"><br>
$item_attayo0
</td></tr>
<tr><td>
エンド1
<input type=text name=e_year0 size=5 value="$e_year0" maxlength="4">年
<input type=text name=e_mon0 size=3 value="$e_mon0" maxlength="2">月
<input type=text name=e_day0 size=3 value="$e_day0" maxlength="2">日
<input type=text name=e_hour0 size=3 value="$e_hour0" maxlength="2">時
<input type=text name=e_min0 size=3 value="$e_min0" maxlength="2">分
<input type=text name=e_sec0 size=3 value="$e_sec0" maxlength="2">秒
</td></tr>
<tr><td>
スタート2 合言葉
<input type=text name=aikotoba2 value="$aikotoba2" maxlength="10">
<input type=text name=s_year1 size=5 value="$s_year1" maxlength="4">年
<input type=text name=s_mon1 size=3 value="$s_mon1" maxlength="2">月
<input type=text name=s_day1 size=3 value="$s_day1" maxlength="2">日
<input type=text name=s_hour1 size=3 value="$s_hour1" maxlength="2">時
<input type=text name=s_min1 size=3 value="$s_min1" maxlength="2">分
<input type=text name=s_sec1 size=3 value="$s_sec1" maxlength="2">秒<br>
分類 $bunluidisp1
<input type=text name=atai1 value="$atai1" maxlength="10">円　または　
<input type=text name=sybetu1 value="$sybetu1" maxlength="10">の
<input type=text name=syouhin1 value="$syouhin1" maxlength="20"><br>
$item_attayo1
</td></tr>
<tr><td>
エンド2
<input type=text name=e_year1 size=5 value="$e_year1" maxlength="4">年
<input type=text name=e_mon1 size=3 value="$e_mon1" maxlength="2">月
<input type=text name=e_day1 size=3 value="$e_day1" maxlength="2">日
<input type=text name=e_hour1 size=3 value="$e_hour1" maxlength="2">時
<input type=text name=e_min1 size=3 value="$e_min1" maxlength="2">分
<input type=text name=e_sec1 size=3 value="$e_sec1" maxlength="2">秒
</td></tr>
<tr><td align="center">
<input type=submit value="書き換え">
</td></tr>
</form>
</table>
</td></tr>
<tr><td>
EOM

		foreach (@sankasya){
			($kaime,$fuku_name,$nichiji,$hinithi) = split(/<>/);
			if($kaime eq $nanba0){
				print "●$nichiji $fuku_name "
			}else{
				print "○$nichiji $fuku_name "
			}
		}


		print <<"EOM";
</td></tr>
</table>
EOM
		&hooter("login_view","戻る");
		exit;

	}else{
		print <<"EOM";
<table border="1"  align=center class=yosumi>
<TR><TD align=center>
EOM
		if($in{'name'} eq $admin_name){
			print <<"EOM";
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="tokuten">
<input type=hidden name=command value="kakikae">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="管理者モード">
</form>
EOM
		}
	}
		if(!$sankaari && $eventon_f){$aikotoba_in="合い言葉 <input type=text name=aikotoba maxlength=\"10\"><input type=submit value=\"ＯＫ\">";}
		print <<"EOM";
<TR><TD align=center>
<center><div class=purasu align=center>＋＋＋合い言葉入力＋＋＋</div><br>
</TD><TR>
<TR><TD align=center>
$mesegi2
$mesegi3
$mesegi4

<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="tokuten">
$aikotoba_in
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=town_no value="$in{'town_no'}">

</form>
</TD></TR>
</table>
EOM
	print "<div align=\"right\">Edit:たっちゃん<div>\n";
	&hooter("login_view","戻る");
	exit;
}		#sub閉じ


