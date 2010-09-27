#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
####################################################################
#　　　　　　　作成　たっちゃん　2006/12/29
#
# 自分の記録ファイル名
$kabu_f = 'mykabu.cgi';
# １銘柄の上限
$konu_jogen = 200;
# 購入許可時間 秒数5*60=300
$koniyu_kyka = 3 * 60;
	
############### town_unit.pl ##################################
#"株" => "<form method=POST action=\"kabu.cgi\"><input type=hidden name=mode value=\"kabu\"><input type=hidden name=mysec value=\"$in{'mysec'}\"><!-- koko2006/04/01 --><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/kabu.gif'  onMouseOver='onMes5(\"株の取引場\")' onMouseOut='onMes5(\"\")'></td></form>",
################################################################

$this_script = 'kabu.cgi';
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
	if($in{'mode'} eq "kabu"){&kabu;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;


sub kabu {
	if ($in{'kouniyu'} =~ /\D/){&error("半角数字のみ有効です。");}

	if (-z "./log_dir/kab_hendou.cgi"){&error("データファイルが壊れました。1"); }
	open(IN,"./log_dir/kab_hendou.cgi") || &error("Open Error : ./log_dir/kab_hendou.cgi");
	$kab_dat = <IN>;
	@ivent_log = <IN>;
	close(IN);
	($kabukaA,$kabukaB,$kabukaC,$kabukaD,$kabukaE,$torihiki,$torihiki_time) = split(/<>/,$kab_dat);

	$ima_time = time;

	if ($ima_time > $torihiki_time){
		$torihiki_mukou = 1;
	}
	$torihiki++;
	$torihiki_time = $ima_time + $koniyu_kyka;

	open (IN, "> ./log_dir/kab_hendou.cgi") || &error("Open Error : ./log_dir/kab_hendou.cgi");
	eval{ flock (IN, 2); };
	print IN "$kabukaA<>$kabukaB<>$kabukaC<>$kabukaD<>$kabukaE<>$torihiki<>$torihiki_time<>\n";
	print IN @ivent_log;
	close (IN);
	if (-z "./log_dir/kab_hendou.cgi"){
		open (IN, "> ./log_dir/kab_hendou.cgi") || &error("Open Error : ./log_dir/kab_hendou.cgi");
		eval{ flock (IN, 2); };
		print IN "$kabukaA<>$kabukaB<>$kabukaC<>$kabukaD<>$kabukaE<>$torihiki<>$torihiki_time<>\n";
		print IN @ivent_log;
		close (IN);
	}
	if (-z "./log_dir/kab_hendou.cgi"){&error("データファイルが壊れました。2"); }

	if (-e "./member/$k_id/$kabu_f"){
		open(IN,"./member/$k_id/$kabu_f") || &error("Open Error : ./member/$k_id/$kabu_f");
		$kabu_all = <IN>;
		$toshikiroku = <IN>;
		@toushirereki = <IN>;
		close(IN);
	}else{
		$kabu_all = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>\n";
		$toshikiroku = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>\n";
		@toushirerek = ();
		open (IN, "> ./member/$k_id/$kabu_f") or &error("Open Error : ./member/$k_id/$kabu_f");
		eval{ flock (IN, 2); };
		print IN $kabu_all;
		print IN $toshikiroku;
		print IN @toushirereki;
		close (IN);
	}
	if ($in{'command'} eq 'del'){
#koko2006/12/31
		($kabuka_A,$kabuka_B,$kabuka_C,$kabuka_D,$kabuka_E,$moti_A,$moti_B,$moti_C,$moti_D,$moti_E,$sisanA,$sisanB,$sisanC,$sisanD,$sisanE) = split(/<>/,$kabu_all);

		$seisan += $kabukaA * $moti_A;
		$seisan += $kabukaB * $moti_B;
		$seisan += $kabukaC * $moti_C;
		$seisan += $kabukaD * $moti_D;
		$seisan += $kabukaE * $moti_E;
		$money += $seisan;
		$kb_display = "$seisan円の精算が行われました。<br>";
#kokoend
		$kabu_all = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>\n";
		$toshikiroku = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>\n";
		@toushirereki = ($kb_display);
		open (IN, "> ./member/$k_id/$kabu_f") or &error("Open Error : ./member/$k_id/$kabu_f");
		eval{ flock (IN, 2); };
		print IN $kabu_all;
		print IN $toshikiroku;
		print IN @toushirereki;
		close (IN);
	}

	($kabuka_A,$kabuka_B,$kabuka_C,$kabuka_D,$kabuka_E,$moti_A,$moti_B,$moti_C,$moti_D,$moti_E,$sisanA,$sisanB,$sisanC,$sisanD,$sisanE) = split(/<>/,$kabu_all);
	($sisanA_0,$sisanA_1,$sisanA_2,$sisanB_0,$sisanB_1,$sisanB_2,$sisanC_0,$sisanC_1,$sisanC_2,$sisanD_0,$sisanD_1,$sisanD_2,$sisanE_0,$sisanE_1,$sisanE_2) = split(/<>/,$toshikiroku);

	if ($torihiki_mukou != 1 && $in{'command'} eq "kau"){
		if ($in{'meigara'} eq "Akabu" && $in{'kouniyu'} != 0){
			if ($in{'kouniyu'} + $moti_A > $konu_jogen){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$kabuka_A = $kabukaA;
				$moti_A += $in{'kouniyu'};
				$sisanA += $kabukaA * $in{'kouniyu'};
				$sisanA0 = $kabukaA * $in{'kouniyu'};
				if($money - $kabukaA * $in{'kouniyu'} < 0){&error("持ち金がありません。");} #2007/03/19
				if($bank - $kabukaA * $in{'kouniyu'} < 0){&error("貯金がありません。");} #2007/03/19
				$money -= $kabukaA * $in{'kouniyu'};
				$kb_display = "大阪株を$kabukaA円にて$in{'kouniyu'}株購入、$sisanA0円投資。";
			}
		}elsif ($in{'meigara'} eq "Bkabu" && $in{'kouniyu'} != 0){
			if ($in{'kouniyu'} + $moti_B > $konu_jogen){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$kabuka_B = $kabukaB;
				$moti_B += $in{'kouniyu'};
				$sisanB += $kabukaB * $in{'kouniyu'};
				$sisanB0 = $kabukaB * $in{'kouniyu'};
				if($money - $kabukaB * $in{'kouniyu'} < 0){&error("持ち金がありません。");} #2007/03/19
				if($bank - $kabukaB * $in{'kouniyu'} < 0){&error("貯金がありません。");} #2007/03/19
				$money -= $kabukaB * $in{'kouniyu'};
				$kb_display = "滋賀株を$kabukaB円にて$in{'kouniyu'}株購入、$sisanB0円投資。";
			}
		}elsif ($in{'meigara'} eq "Ckabu" && $in{'kouniyu'} != 0){
			if ($in{'kouniyu'} + $moti_C > $konu_jogen){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$kabuka_C = $kabukaC;
				$moti_C += $in{'kouniyu'};
				$sisanC += $kabukaC * $in{'kouniyu'};
				$sisanC0 = $kabukaC * $in{'kouniyu'};
				if($money - $kabukaC * $in{'kouniyu'} < 0){&error("持ち金がありません。");} #2007/03/19
				if($bank - $kabukaC * $in{'kouniyu'} < 0){&error("貯金がありません。");} #2007/03/19
				$money -= $kabukaC * $in{'kouniyu'};
				$kb_display = "兵庫株を$kabukaC円にて$in{'kouniyu'}株購入、$sisanC0円投資。";
			}
		}elsif ($in{'meigara'} eq "Dkabu" && $in{'kouniyu'} != 0){
			if ($in{'kouniyu'} + $moti_D > $konu_jogen){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$kabuka_D = $kabukaD;
				$moti_D += $in{'kouniyu'};
				$sisanD += $kabukaD * $in{'kouniyu'};
				$sisanD0 = $kabukaD * $in{'kouniyu'};
				if($money - $kabukadD* $in{'kouniyu'} < 0){&error("持ち金がありません。");} #2007/03/19
				if($bank - $kabukaD * $in{'kouniyu'} < 0){&error("貯金がありません。");} #2007/03/19
				$money -= $kabukaD * $in{'kouniyu'};
				$kb_display = "奈良株を$kabukaD円にて$in{'kouniyu'}株購入、$sisanD0円投資。";
			}
		}elsif ($in{'meigara'} eq "Ekabu" && $in{'kouniyu'} != 0){
			if ($in{'kouniyu'} + $moti_E > $konu_jogen){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$kabuka_E = $kabukaE;
				$moti_E += $in{'kouniyu'};
				$sisanE += $kabukaE * $in{'kouniyu'};
				$sisanE0 = $kabukaE * $in{'kouniyu'};
				if($money - $kabukaA * $in{'kouniyu'} < 0){&error("持ち金がありません。");} #2007/03/19
				if($bank - $kabukaA * $in{'kouniyu'} < 0){&error("貯金がありません。");} #2007/03/19
				$money -= $kabukaE * $in{'kouniyu'};
				$kb_display = "近畿株を$kabukaE円にて$in{'kouniyu'}株購入、$sisanE0円投資。";
			}
		}

	}

	if ($torihiki_mukou != 1 && $in{'command'} eq "uru" && $in{'kouniyu'} != 0){
		if ($in{'meigara'} eq "Akabu"){ 
			if ($moti_A < $in{'kouniyu'}){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$moti_A -= $in{'kouniyu'};
				if ($moti_A <= 0){$kabuka_A = 0;}
				$sisanA = $kabukaA * $moti_A;
				$sisanA1 = $kabukaA * $in{'kouniyu'};
				$money += $kabukaA * $in{'kouniyu'};
				$kb_display = "大阪株を$kabukaA円にて$in{'kouniyu'}株売却、$sisanA1円得ました。";
			}
		}elsif ($in{'meigara'} eq "Bkabu"){ 
			if ($moti_B < $in{'kouniyu'}){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$moti_B -= $in{'kouniyu'};
				if ($moti_B <= 0){$kabuka_B = 0;}
				$sisanB = $kabukaB * $moti_B;
				$sisanB1 = $kabukaB * $in{'kouniyu'};
				$money += $kabukaB * $in{'kouniyu'};
				$kb_display = "滋賀株を$kabukaB円にて$in{'kouniyu'}株売却、$sisanB1円得ました。";
			}
		}elsif ($in{'meigara'} eq "Ckabu"){ 
			if ($moti_C < $in{'kouniyu'}){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$moti_C -= $in{'kouniyu'};
				if ($moti_C <= 0){$kabuka_C = 0;}
				$sisanC = $kabukaC * $moti_C;
				$sisanC1 = $kabukaC * $in{'kouniyu'};
				$money += $kabukaC * $in{'kouniyu'};
				$kb_display = "兵庫株を$kabukaC円にて$in{'kouniyu'}株売却、$sisanC1円得ました。";
			}
		}elsif ($in{'meigara'} eq "Dkabu"){ 
			if ($moti_D < $in{'kouniyu'}){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$moti_D -= $in{'kouniyu'};
				if ($moti_D <= 0){$kabuka_D = 0;}
				$sisanD = $kabukaD * $moti_D;
				$sisanD1 = $kabukaD * $in{'kouniyu'};
				$money += $kabukaD * $in{'kouniyu'};
				$kb_display = "奈良株を$kabukaD円にて$in{'kouniyu'}株売却、$sisanD1円得ました。";
			}
		}elsif ($in{'meigara'} eq "Ekabu"){ 
			if ($moti_E < $in{'kouniyu'}){
				&error("この銘柄の取引上限を超えています。");
			}else{
				$moti_E -= $in{'kouniyu'};
				if ($moti_E <= 0){$kabuka_E = 0;}
				$sisanE = $kabukaE * $moti_E;
				$sisanE1 = $kabukaE * $in{'kouniyu'};
				$money += $kabukaE * $in{'kouniyu'};
				$kb_display = "近畿株を$kabukaE円にて$in{'kouniyu'}株売却、$sisanE1円得ました。";
			}
		}

	}

	if ($torihiki_mukou != 1 && ($in{'command'} eq "kau" || $in{'command'} eq "uru")){

		$sisanA_0 += $sisanA0;
		$sisanA_1 += $sisanA1;
		$sisanA_2 += $sisanA1 - $sisanA0;
		$sisanB_0 += $sisanB0;
		$sisanB_1 += $sisanB1;
		$sisanB_2 += $sisanB1 - $sisanB0;
		$sisanC_0 += $sisanC0;
		$sisanC_1 += $sisanC1;
		$sisanC_2 += $sisanC1 - $sisanC0;
		$sisanD_0 += $sisanD0;
		$sisanD_1 += $sisanD1;
		$sisanD_2 += $sisanD1 - $sisanD0;
		$sisanE_0 += $sisanE0;
		$sisanE_1 += $sisanE1;
		$sisanE_2 += $sisanE1 - $sisanE0;

		$mikomiA = $kabukaA * $moti_A;
		$mikomiB = $kabukaB * $moti_B;
		$mikomiC = $kabukaC * $moti_C;
		$mikomiD = $kabukaD * $moti_D;
		$mikomiE = $kabukaE * $moti_E;

		$all_mikomi = $mikomiA + $mikomiB + $mikomiC + $mikomiD + $mikomiE;
		$deru = $sisanA_0 + $sisanB_0 +$sisanC_0 + $sisanD_0 + $sisanE_0;
		$hairu = $sisanA_1 + $sisanB_1 + $sisanC_1 + $sisanD_1 + $sisanE_1;
		$syushi = $all_mikomi - $deru + $hairu;

		$mouke = $sisanA_2 + $sisanB_2 + $sisanC_2 + $sisanD_2 + $sisanE_2;

		if ($moti_A <= 0){$sisanA_0 = 0;$sisanA_1 = 0;}#$sisanA_2 = 0;}
		if ($moti_B <= 0){$sisanB_0 = 0;$sisanB_1 = 0;}#$sisanB_2 = 0;}
		if ($moti_C <= 0){$sisanC_0 = 0;$sisanC_1 = 0;}#$sisanC_2 = 0;}
		if ($moti_D <= 0){$sisanD_0 = 0;$sisanD_1 = 0;}#$sisanD_2 = 0;}
		if ($moti_E <= 0){$sisanE_0 = 0;$sisanE_1 = 0;}#$sisanE_2 = 0;}

		$toshikiroku = "$sisanA_0<>$sisanA_1<>$sisanA_2<>$sisanB_0<>$sisanB_1<>$sisanB_2<>$sisanC_0<>$sisanC_1<>$sisanC_2<>$sisanD_0<>$sisanD_1<>$sisanD_2<>$sisanE_0<>$sisanE_1<>$sisanE_2<>\n";

		if ($kb_display){
			$kb_display = "$kb_displayで収支は$syushi円見込み。<br>\n";
			unshift @toushirereki,$kb_display;
			if ($#toushirereki + 1 >=10){$#toushirereki =9;}
		}

		open (IN, "> ./member/$k_id/$kabu_f") or &error("Open Error : ./member/$k_id/$kabu_f");
		eval{ flock (IN, 2); };
		$kabu_all = "$kabuka_A<>$kabuka_B<>$kabuka_C<>$kabuka_D<>$kabuka_E<>$moti_A<>$moti_B<>$moti_C<>$moti_D<>$moti_E<>$sisanA<>$sisanB<>$sisanC<>$sisanD<>$sisanE<>\n";
		print IN $kabu_all;
		print IN $toshikiroku;
		print IN @toushirereki;
		close (IN);

#		$torihiki--;
#		open (IN, "> ./log_dir/kab_hendou.cgi") || &error("Open Error : ./log_dir/kab_hendou.cgi");
#		eval{ flock (IN, 2); };
#		print IN "$kabukaA<>$kabukaB<>$kabukaC<>$kabukaD<>$kabukaE<>$torihiki<>$torihiki_time<>\n";
#		print IN @ivent_log
#		close (IN);
	}else{
		if ($torihiki_mukou == 1){
			$disp = "<br><b>$koniyu_kyka秒タイムアウト再取引を開始します。</b><br>\n";
		}
	}
#	&header(ginkou_style);


	$A_moti_disp = $konu_jogen - $moti_A;
	$A_goukei = $kabukaA * $moti_A;
	$A_moti_disp2 = "$kabuka_A × $moti_A";
	if ($moti_A != 0){
		$motitankaA = int($sisanA / $moti_A);
		$moukeA = $kabukaA * $moti_A - $sisanA;
	}else{
		$motitankaA = 0;
		$moukeA = 0;
	}

	$B_moti_disp = $konu_jogen - $moti_B;
	$B_goukei = $kabukaB * $moti_B;
	$B_moti_disp2 = "$kabuka_B × $moti_B";
	if ($moti_B != 0){
		$motitankaB = int($sisanB / $moti_B);
		$moukeB = $kabukaB * $moti_B - $sisanB;
	}else{
		$motitankaB = 0;
		$moukeB = 0;
	}

	$C_moti_disp = $konu_jogen - $moti_C;
	$C_goukei = $kabukaC * $moti_C;
	$C_moti_disp2 = "$kabuka_C × $moti_C";
	if ($moti_C != 0){
		$motitankaC = int($sisanC / $moti_C);
		$moukeC = $kabukaC * $moti_C - $sisanC;
	}else{
		$motitankaC = 0;
		$moukeC = 0;
	}

	$D_moti_disp = $konu_jogen - $moti_D;
	$D_goukei = $kabukaD * $moti_D;
	$D_moti_disp2 = "$kabuka_D × $moti_D";
	if ($moti_D != 0){
		$motitankaD = int($sisanD / $moti_D);
		$moukeD = $kabukaD * $moti_D - $sisanD;
	}else{
		$motitankaD = 0;
		$moukeD = 0;
	}

	$E_moti_disp = $konu_jogen - $moti_E;
	$E_goukei = $kabukaE * $moti_E;
	$E_moti_disp2 = "$kabuka_E × $moti_E";
	if ($moti_E != 0){
		$motitankaE = int($sisanE / $moti_E);
		$moukeE = $kabukaE * $moti_E - $sisanE;
	}else{
		$motitankaE = 0;
		$moukeE = 0;
	}

	$ima_time = $torihiki_time;

	&header(ginkou_style);
	print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="0" align="center" width="80%">
<tr><td colspan="2">
<div class=midasi align=center>++ 株取引 ++</div><div align=center>
$disp
<tr><td colspan="2">
<br>
株の買い付けは$konu_jogen迄と致します。<br>
<br>
</td></tr>
<tr><td>
<form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
大阪株 $kabukaA × $moti_A
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="kau">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Akabu">
<input type=hidden name=motteru value="$A_moti_disp">
<input type=text name=kouniyu size=3 maxlength=3 value="$A_moti_disp">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="購入する">
</form>
</td><td><form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
大阪持ち株 $A_moti_disp2 の内
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="uru">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Akabu">
<input type=hidden name=motteru value="$moti_A">
<input type=text name=kouniyu size=3 maxlength=3 value="$moti_A">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="売却する">
</form>
</td></tr>
<tr><td>
持ってる平均株価は$sisanA÷$moti_A＝$motitankaA です。<br>
</td><td>
この持ち株を売れば、$moukeA の損益です。<br>
</td></tr>
<tr><td colspan="2">
投資$sisanA_0円 回収$sisanA_1円収支$sisanA_2円
</td></tr>

<tr><td>
<form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
滋賀株 $kabukaB × $moti_B
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="kau">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Bkabu">
<input type=hidden name=motteru value="$moti_B">
<input type=text name=kouniyu size=3 maxlength=3 value="$B_moti_disp">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="購入する">
</form>
</td><td><form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
滋賀持ち株 $B_moti_disp2 の内
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="uru">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Bkabu">
<input type=hidden name=motteru value="$moti_B">
<input type=text name=kouniyu size=3 maxlength=3 value="$moti_B">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="売却する">
</form>
</td></tr>
<tr><td>
持ってる平均株価は$sisanB÷$moti_B＝$motitankaB です。<br>
</td><td>
この持ち株を売れば、$moukeB の損益です。<br>
</td></tr>
<tr><td colspan="2">
投資$sisanB_0円 回収$sisanB_1円収支$sisanB_2円
</td></tr>

<tr><td>
<form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
兵庫株 $kabukaC × $moti_C
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="kau">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Ckabu">
<input type=hidden name=motteru value="$moti_C">
<input type=text name=kouniyu size=3 maxlength=3 value="$C_moti_disp">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="購入する">
</form>
</td><td><form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
兵庫持ち株 $C_moti_disp2 の内
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="uru">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Ckabu">
<input type=hidden name=motteru value="$moti_C">
<input type=text name=kouniyu size=3 maxlength=3 value="$moti_C">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="売却する">
</form>
</td></tr>
<tr><td>
持ってる平均株価は$sisanC÷$moti_C＝$motitankaC です。<br>
</td><td>
この持ち株を売れば、$moukeC の損益です。<br>
</td></tr>
<tr><td colspan="2">
投資$sisanC_0円 回収$sisanC_1円収支$sisanC_2円
</td></tr>

<tr><td>
<form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
奈良株 $kabukaD × $moti_D
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="kau">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Dkabu">
<input type=hidden name=motteru value="$moti_D">
<input type=text name=kouniyu size=3 maxlength=3 value="$D_moti_disp">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="購入する">
</form>
</td><td><form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
奈良持ち株 $D_moti_disp2 の内
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="uru">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Dkabu">
<input type=hidden name=motteru value="$moti_D">
<input type=text name=kouniyu size=3 maxlength=3 value="$moti_D">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="売却する">
</form>
</td></tr>
<tr><td>
持ってる平均株価は$sisanD÷$moti_D＝$motitankaD です。<br>
</td><td>
この持ち株を売れば、$moukeD の損益です。<br>
</td></tr>
<tr><td colspan="2">
投資$sisanD_0円 回収$sisanD_1円収支$sisanD_2円
</td></tr>

<tr><td>
<form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
近畿株 $kabukaE × $moti_E
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="kau">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Ekabu">
<input type=hidden name=motteru value="$moti_E">
<input type=text name=kouniyu size=3 maxlength=3 value="$E_moti_disp">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="購入する">
</form>
</td><td><form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
近畿持ち株 $E_moti_disp2 の内
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="uru">
<input type=hidden name=torihiki value="$ima_time">
<input type=hidden name=meigara value="Ekabu">
<input type=hidden name=motteru value="$moti_E">
<input type=text name=kouniyu size=3 maxlength=3 value="$moti_E">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="売却する">
</form>
</td></tr>
<tr><td>
持ってる平均株価は$sisanE÷$moti_E＝$motitankaE です。<br>
</td><td>
この持ち株を売れば、$moukeE の損益です。<br>
</td></tr>
<tr><td colspan="2">
投資$sisanE_0円 回収$sisanE_1円収支$sisanE_2円
</td></tr>
</table>
EOM

	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="0" align="center" width="80%">
<tr><td>

<form method=\"POST\" name=kabu_a0 action="$this_script" style="margin-bottom: 0em">
<input type=hidden name=mode value="kabu">
<input type=hidden name=command value="del">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="記録消去">持ち株が消えますので売ってから押してください。
</form>
<b>売買記録</b><br>@toushirereki</td></tr></table>
EOM



	print "<table border=\"1\" bgcolor=\"#ffffff\" cellspacing=\"0\" cellpadding=\"0\" align=\"center\" width=\"80%\">\n";
	print "<tr><td><b>株価動向</b><br>\n@ivent_log</td></tr></table>\n";

	print "<div align=\"right\">Edit:たっちゃん<div>\n";

	&hooter("login_view","戻る");



	exit;
}		#sub閉じ

