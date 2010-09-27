#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
# 合成屋
#　 Edit:たっちゃん　2007/11/01
#################################
# 合成データファイル
$gousei_f = './dat_dir/gousei.cgi';

# 合成品に限定('yes')持ち物全体にする('no')
$gouseihinnomi = 'no';#'yes';#'no';
################################
# unit.pl
#"合成" => "<form method=POST action=\"gouseiya.cgi\"><input type=hidden name=mode value=\"gousei\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/gouseiyai.gif'  onMouseOver='onMes5(\"合成して品物を作ります。\")' onMouseOut='onMes5(\"\")'></td></form>\n",
################################
# dat_dir/syouhin 追加
#合成<>冷蔵庫<>0<>0<>5<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>500<>0<>0<>0<>10<>回<>1<>5<>0<><>0<>0<>冷やします<><><><>
#合成<>ポット<>0<>0<>5<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>500<>0<>0<>0<>10<>回<>1<>5<>0<><>0<>0<>暖めます<><><><>
#合成<>コーヒー豆<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>500<>0<>5<>0<>1<>回<>1<>5<>0<><>0<>0<>よい香りがします<><><><>
#合成<>コーヒー<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>500<>0<>5<>0<>1<>回<>1<>5<>0<><>0<>0<>よい香りがします<><><><>
#ドリンク<>ミルク<>0<>0<>0<>0<>1<>1<>0<>無<>0<>0<>0<>0<>0<>0<>0<>200<>0<>0<>0<>1<>回<>30<>30<>100<><><><><>0<>0<>0<>
#
#　つづく
# dat_dir/gousei.cgi 作成
#ドリンク<>アイスコーヒー=冷蔵庫:1+コーヒー豆:1<>0<>0<>0<>0<>0<>1<>0<>無<>1<>0<>0<>0<>0<>0<>0<>200<>0<>0<>0<>1<>回<>30<>30<>100<><><><><>0<>0<>0<>
#ドリンク<>ホットコーヒー=ポット:1+コーヒー豆:1<>0<>0<>0<>0<>0<>1<>0<>無<>1<>0<>0<>0<>0<>0<>0<>200<>0<>0<>0<>1<>回<>30<>30<>100<><><><><>0<>0<>0<>
#ドリンク<>焙煎アイスコーヒー=冷蔵庫:1+コーヒー豆:1<>0<>0<>0<>0<>0<>1<>0<>無<>1<>0<>0<>0<>0<>0<>0<>200<>0<>0<>0<>1<>回<>30<>30<>100<><><><><>0<>0<>0<>
#ドリンク<>焙煎ホットコーヒー=ポット:1+コーヒー豆:1<>0<>0<>0<>0<>0<>1<>0<>無<>1<>0<>0<>0<>0<>0<>0<>200<>0<>0<>0<>1<>回<>30<>30<>100<><><><><>0<>0<>0<>
#ドリンク<>ミルクコーヒー=ポット:1+コーヒー:1+ミルク:1<>0<>0<>0<>0<>0<>1<>0<>無<>1<>0<>0<>0<>0<>0<>0<>200<>0<>0<>0<>1<>回<>30<>30<>100<><><><><>0<>0<>0<>
#食料品<>アイスクリーム=冷蔵庫:1:+ミルク:2<>0<>0<>0<>0<>0<>1<>0<>無<>1<>0<>0<>0<>0<>0<>0<>200<>0<>0<>0<>1<>回<>30<>30<>100<><><><><>0<>0<>0<>
# つづく
#################################

$this_script = 'gouseiya.cgi';
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
	if($in{'mode'} eq "gousei"){&gousei;}
	if($in{'mode'} eq "gousei_do"){&gousei_do;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub gousei{
	open(IN,"< $gousei_f") || &error("$gousei_fが開けません");
	eval{ flock (IN, 1); };
	@mygosei_hairetu = <IN>;
	close(IN);
	foreach $gousei (@mygosei_hairetu){
		&syouhin_sprit($gousei);
		$syo_syubetu0 = $syo_syubetu;
		($syo_hinmoku0,$moto) = split(/\=/,$syo_hinmoku);
		($zairyou1,$zairyou2,$zairyou3) = split(/\+/,$moto);

		$aru = 0;
		($genryo1,$kosu1) = split(/\:/,$zairyou1);
		foreach (@genryoulist){
			if ($_ eq $genryo1){$aru=1;}
		}
		if(!$aru){push @genryoulist,$genryo1;}

		$aru = 0;
		($genryo2,$kosu2) = split(/\:/,$zairyou2);
		foreach (@genryoulist){
			if ($_ eq $genryo2){$aru=1;}
		}
		if(!$aru){push @genryoulist,$genryo2;}

		$aru = 0;
		if($zairyou3){
			($genryo3,$kosu3) = split(/\:/,$zairyou3);
			foreach (@genryoulist){
				if ($_ eq $genryo3){$aru=1;}
			}
			if(!$aru){push @genryoulist,$genryo3;}
			$aru = 0;
		}
	}

	$my_item_f = "./member/$k_id/mono.cgi";
	open(IN,"< $my_item_f") || &error("$my_item_fが開けません");
	eval{ flock (IN, 1); };
	@myitem_hairetu = <IN>;
	close(IN);

	&header(item_style);

	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>交換の手数料は0円です。<br>ＯＫの左には作成したい個数を入れることも可能\です。<br>
	※自分で作成した「合成品」は持ち物アイテムに現れます。<br>
	<td  bgcolor=#00ffbf align=center width="200"><h1>合成屋</h1></td>
	</tr></table><br>
	
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td>
EOM

	if($gouseihinnomi eq 'yes'){
		foreach $tmp (@myitem_hairetu){
			&syouhin_sprit($tmp);
			if ($syo_syubetu eq "合成"){
				if($syo_taikyuu > 0){
					if ($syo_taikyuu_tani eq "日"){
						$keikanissuu = int ((time - $syo_kounyuubi) / (60*60*24));
						$syo_taikyuu = int($syo_taikyuu - $keikanissuu);
					}
					if($syo_taikyuu > 0){
						print "$syo_hinmoku × $syo_taikyuu あります。<br>\n";
						&syouhin_temp;
						push @goseihinmoku,$syo_temp;
					}
				}
			}
		}
	}else{
		foreach $tmp (@myitem_hairetu){
			&syouhin_sprit($tmp);
			if($syo_taikyuu > 0){
				foreach $tmp2 (@genryoulist){
					if ($tmp2 && $syo_hinmoku eq $tmp2){
						if ($syo_taikyuu_tani eq "日"){
							$keikanissuu = int ((time - $syo_kounyuubi) / (60*60*24));
							$syo_taikyuu = int($syo_taikyuu - $keikanissuu);
						}
						if($syo_taikyuu > 0){
							print "$syo_hinmoku × $syo_taikyuu あります。<br>\n";
							&syouhin_temp;
							push @goseihinmoku,$syo_temp;
						}
					}
				}
			}
		}
	}

	print <<"EOM";
	<br><hr>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="gousei_do">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
EOM

	foreach $gousei (@mygosei_hairetu){
		&syouhin_sprit($gousei);
		$seizou = 0;
		$item = 0;
		$syo_syubetu0 = $syo_syubetu;
		($syo_hinmoku0,$moto) = split(/\=/,$syo_hinmoku);
		($zairyou1,$zairyou2,$zairyou3) = split(/\+/,$moto);
		if($zairyou3){$item3 = 3;}else{$item3 = 2;}
		$item_mothi1=0;
		$item_mothi2=0;
		$item_mothi3=0;

		($genryo1,$kosu1) = split(/\:/,$zairyou1);
		foreach $temp (@goseihinmoku){
			&syouhin_sprit($temp);
			if($syo_hinmoku eq $genryo1 && !$item_mothi1){
				$saidai = int($syo_taikyuu / $kosu1);
			#	if($saidai > $saidai_max){$saidai = $saidai_max;} #koko2007/10/28 修正
				$item++;
				$item_mothi1=1;
				last;
			}
		}
		($genryo2,$kosu2) = split(/\:/,$zairyou2);
		foreach $temp (@goseihinmoku){
			&syouhin_sprit($temp);
			if($syo_hinmoku eq $genryo2 && !$item_mothi2){
				$saidai_max =int($syo_taikyuu / $kosu2);
				if($saidai > $saidai_max){$saidai = $saidai_max;}
				$item++;
				$item_moth2=1;
				last;
			}
		}


		if($zairyou3 && !$item_mothi3){
			($genryo3,$kosu3) = split(/\:/,$zairyou3);
			foreach $temp (@goseihinmoku){
				&syouhin_sprit($temp);
				if($syo_hinmoku eq $genryo3 && !$item_mothi3){
					$saidai_max =int($syo_taikyuu / $kosu3);
					if($saidai > $saidai_max){$saidai = $saidai_max;}
					$item++;
					$item_mothi3 = 1;
					last;
				}
			}
		}

		if($item == $item3 && $saidai > 0){
			$sakusidekiru = 1;
			&syouhin_sprit($gousei); #koko2007/10/18
			$totalu = $saidai * $syo_taikyuu;
			print "<input type=\"radio\" name=\"kakou\" value=\"$syo_hinmoku0-$saidai-$syo_taikyuu\">\n"; #koko2007/10/18
			print "$syo_syubetu0 の $syo_hinmoku0 が $saidai個 × $syo_taikyuu組 ＝ $totaluセット製造可能\です。<br>\n"; #koko2007/10/18
		}
	}
	if(!$sakusidekiru){print "作成できる品物はありません。<br>\n";}

	print <<"EOM";
	<div align=center>
	<input type=\"text\" name=\"seizou\" size=\"2\" value=\"\" maxlength=\"2\">個 
	<input type=submit value=" O K ">
	<input type="reset">
	</div></form></td></tr>
	</table>
EOM

	&hooter("login_view","戻る");
	exit;

}

sub gousei_do{
	$my_item_f = "./member/$k_id/mono.cgi";
	open(IN,"< $my_item_f") || &error("$my_item_fが開けません");
	eval{ flock (IN, 1); };
	@myitem_hairetu = <IN>;
	close(IN);

	($tukuru,$syouhi,$moto_taikyuu) = split(/\-/,$in{'kakou'}); #koko2007/10/18
#	($syouhi,$set) = split(/\:/,$syouhi);
	if($in{'seizou'} && $in{'seizou'} < $syouhi && $syouhi > 0){$syouhi = $in{'seizou'};}
	if(!$tukuru){&error("製造商品が選ばれていません。");}

	open(IN,"< $gousei_f") || &error("$gousei_fが開けません");
	eval{ flock (IN, 1); };
	@mygosei_hairetu = <IN>;
	close(IN);

	foreach $gousei (@mygosei_hairetu){
		&syouhin_sprit($gousei);
		$seizou = 0;
		$item = 0;
		$syo_syubetu0 = $syo_syubetu;
		($syo_hinmoku0,$moto) = split(/\=/,$syo_hinmoku);
		
		if($syo_hinmoku0 ne $tukuru){next;}
		$gousei0 = $gousei;
		$syo_taikyuu0 = $syo_taikyuu;
		($zairyou1,$zairyou2,$zairyou3) = split(/\+/,$moto);
		if($zairyou3){$item3 = 3;}else{$item3 = 2;}
		$item_mothi1=0;
		$item_mothi2=0;
		$item_mothi3=0;

		$i = 0;
		($genryo1,$kosu1) = split(/\:/,$zairyou1);
		foreach $temp (@myitem_hairetu){
			&syouhin_sprit($temp);
			if($gouseihinnomi eq "yes"){
				unless ($syo_syubetu eq "合成" && $syo_hinmoku eq $genryo1 && !$item_mothi1){
					$i++;
					next;
				}
			}elsif(!($syo_hinmoku eq $genryo1 && !$item_mothi1)){
				$i++;
				next;
			}
			if($syo_taikyuu <=0){&error("材料がありません。");} #koko2007/11/01
			$syo_taikyuu -= $kosu1 * $syouhi;
			$item++;
			$item_mothi1=1;
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
			last;
		}
		($genryo2,$kosu2) = split(/\:/,$zairyou2);
		$i = 0;
		foreach $temp (@myitem_hairetu){
			&syouhin_sprit($temp);
			if($gouseihinnomi eq "yes"){
				unless ($syo_syubetu eq "合成" && $syo_hinmoku eq $genryo2 && !$item_mothi2){
					$i++;
					next;
				}
			}elsif(!($syo_hinmoku eq $genryo2 && !$item_mothi2)){
				$i++;
				next;
			}
			if($syo_taikyuu <=0){&error("材料がありません。");} #koko2007/11/01
			$syo_taikyuu -= $kosu2 * $syouhi;
			$item++;
			$item_moth2=1;
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
			last;
		}
		if($zairyou3 && !$item_mothi3){
			($genryo3,$kosu3) = split(/\:/,$zairyou3);
			$i = 0;

			foreach $temp (@myitem_hairetu){
				&syouhin_sprit($temp);
				if($gouseihinnomi eq "yes"){
					unless ($syo_syubetu eq "合成" && $syo_hinmoku eq $genryo3 && !$item_mothi3){
						$i++;
						next;
					}
				}elsif(!($syo_hinmoku eq $genryo3 && !$item_mothi3)){
					$i++;
					next;
				}
				if($syo_taikyuu <=0){&error("材料がありません。");} #koko2007/11/01
				$syo_taikyuu -= $kosu3 * $syouhi;
				$item++;
				$item_mothi3 = 1;
				&syouhin_temp;
				$myitem_hairetu[$i] = $syo_temp;

				last;
			}
		}
	}
# 同一製品作成の場合の処理
	$motmon_attuta = 0;
	$i = 0;
	foreach	(@myitem_hairetu){
		&syouhin_sprit($_);
		if($syo_hinmoku eq $tukuru){
			$syo_taikyuu += $moto_taikyuu * $syouhi; #koko2007/10/18
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
			$motmon_attuta = 1;
			last;
		}
		$i++
	}
# 新しい商品の場合
	if(!$motmon_attuta){
		foreach	$tmp(@mygosei_hairetu){
			&syouhin_sprit($tmp);
			($syo_hinmoku0,$moto) = split(/\=/,$syo_hinmoku);
			if($syo_hinmoku0 eq $tukuru){
				&syouhin_sprit($tmp);
				$syo_taikyuu = $moto_taikyuu * $syouhi; #koko2007/10/18
				$syo_hinmoku = $tukuru;
				$syo_kounyuubi = time;
				&syouhin_temp;
				push @myitem_hairetu,$syo_temp;
				last;
			}
		}
	}

	open(OUT,"> $my_item_f") || &error("$my_item_fが開けません");
	eval{ flock (OUT, 2); };
	print OUT @myitem_hairetu;
	close(OUT);

	$print_messe = "$tukuru を $syouhi個、作成しました。";

	&header("","item_style");

	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
$print_messe
</span>
</td></tr></table>
<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="gousei">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="加工に戻る">
	</form>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
	exit;
}

