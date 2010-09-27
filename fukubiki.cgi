#!/usr/bin/perl

#################################
# 参加済みファイル　新しいイベントの時は空にする。
$sankazumi = "./log_dir/fukubikisanka.cgi";
#画像ファイルのディレクトリ
$img_dir2 = "./sugoroku/img";
# 景品データ
$keihin_f = "./dat_dir/keihin.cgi";
# カードの枚数 2から4　それ以外は無効
$kado_kazu =1;
# 開始日の指定　年、月、日、時、分、秒
$s_year = 2007;$s_mon = 9;$s_day = 10;$s_hour = 12;$s_min = 0;$s_sec =0;
# 終了日の指定　年、月、日、時、分、秒
$e_year = 2010;$e_mon = 1;$e_day = 3;$e_hour = 12;$e_min = 0;$e_sec =0;
# 箱が１つになり全商品から何か１つ当たる 'yes','no'
$hazure_nashi = 'yes';
# 管理者動作チェックの時　$test = "1";# "", "0"
$test = "";#
# １日の引くことが出来る回数
$hiku_kaisu = 1;
#######################################

$this_script = 'fukubiki.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}

#条件分岐
	if (!$test){
		use Time::Local;
		eval{ $s_tim = timelocal($s_sec, $s_min, $s_hour, $s_day, $s_mon -1, $s_year); };
		$mond = sprintf("%02d",$s_mon);
		$mdayd = sprintf("%02d",$s_day);
		$mind = sprintf("%02d",$s_min);
		$secd = sprintf("%02d",$s_sec);

		eval{ $e_tim = timelocal($e_sec, $e_min, $e_hour, $e_day, $e_mon -1, $e_year); };
		$mond2 = sprintf("%02d",$e_mon);
		$mdayd2 = sprintf("%02d",$e_day);
		$mind2 = sprintf("%02d",$e_min);
		$secd2 = sprintf("%02d",$e_sec);

		if ($s_tim >= $e_tim){&error("開始日時か終了日時にミスがあります。")}

		$ima_tine = time;
		if ($s_tim > $ima_tine){
			if (not(-z $sankazumi)) {
				open (DAT, "> $sankazumi") or die("エラー・$sankazumiファイルが開けません");
				eval{ flock (DAT, 2); };
				print DAT "";
				close (DAT);
			}

			&error("イベントは、$s_year/$mond/$mdayd $s_hour:$mind:$secd より、$e_year/$mond2/$mdayd2 $e_hour:$mind2:$secd2 の間行われます。");
		}elsif($e_tim < $ima_tine){ #参加した人のリストは残っています。
			&error("イベントは、$e_year/$mond2/$mdayd2 $e_hour:$mind2:$secd2 に終了しました。");
		}
	}

	if(!$in{'k_id'}){&error("mono.cgi エラー hanbai1")}
	$monokiroku_file="./member/$in{'k_id'}/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
		$motimonokensa = '';
		foreach (@my_kounyuu_list){
			&syouhin_sprit ($_);
			if ($syo_hinmoku eq '福引券'){
				$motimonokensa = 1;
				last;
			}
	}
		if (!$motimonokensa){&error("福引券がないとは入れません。<br>福引券はクーポンで交換できます。");}
	
	if($in{'mode'} eq "fukubiki"){&fukubiki;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub fukubiki {
	
	open(MA,"< $sankazumi") || &error("$sankazumiが開けません");
	eval{ flock (MK, 1); };
	@sankasya = <MA>;
	close(MA);

	if(!$k_id){&error("mono.cgi エラー fukubiki1")}
	$monokiroku_file="./member/$in{'k_id'}/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);

	$motikazu = 0;
	foreach (@my_item_list){
		&syouhin_sprit($_);
		if ($syo_syubetu eq 'ギフト' || $syo_syubetu eq 'ギフト商品' || $syo_taikyuu <= 0){next;}
		$motikazu++;
	}
	if ($motikazu >= $syoyuu_gendosuu){&error("持ち物が上限だったので、諦めた。$motikazu/$syoyuu_gendosuu");} #koko2007/09/17

	(@time_local)=localtime(time);
	$i = 0;
	foreach (@sankasya){
		($fuku_name,$kaisu,$hinithi) = split(/<>/);
		chomp $hinithi;
		if ($test){$hinithi = 0;}
		if ($time_local[3] ne $hinithi){
			$kaisu = 0;
		}
		if ($in{'name'} eq $fuku_name && $kaisu >= $hiku_kaisu && $time_local[3] eq $hinithi){&error("１日$hiku_kaisu回しか参加できません。");}
		$hinithi = $time_local[3];
		if ($in{'name'} eq $fuku_name){
			$name_ari = 1;
			if ($in{'command'} eq "hiku"){
				$basyo = $i;
				last;
			}
		}
		$i++;
	}
	
	if ($kaisu ne "" && $in{'command'} eq "hiku"){
		if(!$test){$kaisu++;}
		$sankasya[$basyo] = "$in{'name'}<>$kaisu<>$hinithi<>\n";
	}elsif(!$name_ari){
		push @sankasya,"$in{'name'}<>0<>$hinithi<>\n";
	}
	
	open(MA,"> $sankazumi") || &error("$sankazumiが開けません");
	eval{ flock (MA, 2); };
	print MA @sankasya;
	close(MA);

	&header(ginkou_style);

	if ($in{'command'} eq "hiku"){

		open(MA,"< $keihin_f") || &error("$keihin_fが開けません");
		eval{ flock (MK, 1); };
		@keihin = <MA>;
		close(MA);

		if($hazure_nashi ne 'yes'){
			$i = 0;
			foreach (@keihin){
				&syouhin_sprit($_);
				if ($syo_syubetu eq '当たり'){
					push @atari,$keihin[$i];
				}elsif ($syo_syubetu eq '並'){
					push @nami,$keihin[$i];
				}else{
					push @hazure,$keihin[$i];
				}
				$i++;
			}
			#データ読み込み
			$wid = 100 * $kado_kazu;
		}else{
			$wid = "100%";
		}

		print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<TR><TD align=center>
<div class=purasu align=center>＋＋＋結果発表\＋＋＋</div>
<table border=0 bgcolor=#ffffff cellspacing=0 cellpadding=3 align=center width=$wid><tr>
EOM

		if($hazure_nashi ne 'yes'){
			@randed = &randcheck($kado_kazu,$kado_kazu);
			for($i=1;$i < $kado_kazu + 1 ;$i++){
				if($in{'sentaku_card'} == $i){
					$koredaro="<div align=center>↑<br>選んだカード</div>";
					if($i == $randed[0]){
						$keihin = $atari[int(rand($#atari+1))];
						&syouhin_sprit($keihin);
						$disp = "<div class=purasu align=center>$syo_hinmokuが見事当たりました！</div>\n";

					}elsif($i == $randed[1] && $kado_kazu >= 3){
						$keihin = $nami[int(rand($#nami+1))];
						&syouhin_sprit($keihin);
						$disp = "<div class=mainasu align=center>並の$syo_hinmokuですね。</div>\n";
					}elsif($i == $randed[2] && $kado_kazu == 4){
						$keihin = $nami[int(rand($#nami+1))];
						&syouhin_sprit($keihin);
						$disp = "<div class=mainasu align=center>並の$syo_hinmokuですね。</div>\n";
#はずれた場合
					}else{
						$keihin = $hazure[int(rand($#hazure+1))];
						&syouhin_sprit($keihin);
						$disp = "<div class=mainasu align=center>$syo_hinmokuだ、はずれてしまいました。</div>\n";
					}
				}else{
					$koredaro="";

				}

				if($i == $randed[0]){
					print "<td><img src=$img_dir/fuku.gif width=90 height=109>$koredaro</td>\n";

				}elsif($i == $randed[1] && $kado_kazu >=3){
					print "<td><img src=$img_dir/fuku.gif width=90 height=109>$koredaro</td>\n";
				}elsif($i == $randed[2] && $kado_kazu ==4){
					print "<td><img src=$img_dir/fuku.gif width=90 height=109>$koredaro</td>\n";
				}else{
					print "<td><img src=$img_dir/fuku.gif width=90 height=109>$koredaro</td>\n";
				}
			}
		}else{
			$keihin = $keihin[int(rand($#keihin+1))];
			&syouhin_sprit($keihin);
			$disp = "<div class=purasu align=center>$syo_hinmokuが当たりました！</div>\n";
			print "<td align=center><img src=$img_dir/fuku.gif width=90 height=109>$koredaro</td>\n";
		}
#koko2007/09/14
		$syo_kounyuubi = time;
		&syouhin_temp;

		print "</tr><tr><td colspan=$kado_kazu>";
		print "$disp\n";
		print "</td></tr></table>";

		if(!$test){push @my_item_list,$syo_temp;} #koko2007/09/14
		open(OUT,"> $monokiroku_file") || &error("自分の購入物ファイルが開けません");
		eval{ flock (OUT, 2); };
		print OUT @my_item_list;
		close(OUT);

		print <<"EOM";
<table border="1"  align=center class=yosumi>
<TR><TD align=center>
<center>
 もらった商品：$syo_hinmoku <BR>
<TD><TR>
</table></table>
EOM

	}else{		#if（引くコマンドだったら）の閉じ
		$wid = 100 * $kado_kazu;
		print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<TR><TD align=center>
<center><div class=purasu align=center>＋＋＋プレゼントゲーム＋＋＋</div><br>
</TD><TR>
</table>
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<tr><td>
<table border="0" cellspacing="0" cellpadding="3" align="center" width="$wid">
<tr>
EOM
		if ($kado_kazu >=1){
			print <<"EOM";
<td align="center">
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="fukubiki">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=image src="$img_dir/fukubiki1.GIF" width="90" height="110">
<input type="hidden" name="sentaku_card" value="1">
</form></td>
EOM
}
		if ($kado_kazu >=2){
			print <<"EOM";
<td align="center">
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="fukubiki">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=image src="$img_dir2/card_sentaku.gif" width="90" height="110">
<input type="hidden" name="sentaku_card" value="2">
</form></td>
EOM
}
		if ($kado_kazu >=3){
			print <<"EOM";
<td align="center">
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="fukubiki">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=image src="$img_dir2/card_sentaku.gif" width="90" height="110">
<input type="hidden" name="sentaku_card" value="3">
</form></td>
EOM
		}
		if ($kado_kazu ==4){
			print <<"EOM";
<td align="center">
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="fukubiki">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=image src="$img_dir2/card_sentaku.gif" width="90" height="110">
<input type="hidden" name="sentaku_card" value="4">
</form></td>
EOM
		}
		print <<"EOM";
</tr></table>
<div align="center">
カードをクリックしてください。</div>
</td>
</tr>
</table>
EOM
	}		#else（引くコマンドで無い場合）の閉じ

	print "<div align=\"right\">Edit:たっちゃん<div>\n";

	&hooter("login_view","戻る");
	exit;
}		#sub閉じ

##### くじ引き　01 以上 $_[0] 以下の数字を $_[1] 個選び返す
sub randcheck {
	my @list = ();
	my $str = "";
	my $i = 0;
	while ($i < $_[1]) {
		my $tmp = sprintf("%02d",(rand($_[0]))+1);
		if (index($str, $tmp) < 0) {
			$str .= ",$tmp";
			$i++;
		}
	}
	@list = split /,/,$str;
	shift(@list);	# 先頭の空要素取り除き
	return (@list);
}

