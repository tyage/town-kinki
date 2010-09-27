#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
##############################################
# 販売商品の入ったデータファイル
$syohin_file = './dat_dir/soubi.cgi';
##############################################

$this_script = 'hanbai.cgi';
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
	if($in{'mode'} eq "hanbai"){&hanbai;}
	if($in{'mode'} eq 'buy'){&buy;}
	if($in{'mode'} eq 'soubi'){&soubi;}
	if($in{'mode'} eq 'soubi_do'){&soubi_do;}
	if($in{'mode'} eq 'kajiya'){&kajiya;}
	if($in{'mode'} eq 'kajiya_do'){&kajiya_do;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

########################################################################
sub hanbai{
	open(IN,"$syohin_file") || &error("Open Error : $syohin_file");
	eval{ flock (IN, 2); };
	@syohin_data=<IN>;
	close(IN);
	
	foreach(@syohin_data){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_nedan,$syo_kaisuu)=split(/<>/);
	     if($syo_syu eq "武器"){
	     	     $syo_buki .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_nedan</td></tr>";
	     }elsif($syo_syu eq "防具"){
	     	     $syo_bougu .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_nedan</td></tr>";
	     }elsif($syo_syu eq "魔法"){
	     	     $syo_mahousyo .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_nedan</td></tr>";
	     }elsif($syo_syu eq "御守"){
	     	     $syo_omamori .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_nedan</td></tr>";
	     }
	}
	
	&header(gym_style);
	print <<"EOM";
	<table border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td>
	<table><form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>soubi<>">
	<tr><td colspan=5><center><input type="submit" value="倉庫へ行く"></center></td></tr>
	</form></table>
	</td><td>
	<table><form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>kajiya<>">
	<tr><td colspan=5><center><input type="submit" value="鍛冶屋へ行く"></center></td></tr>
	</form></table>
	</td></tr>
	</table>
	<br>
	<table border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>buy<>">
	<tr bgcolor=#ccff33><td align=center nowrap>商品名</td><td align=center nowrap>威力</td><td>命中率（％）</td><td>使用可\能\回\数</td><td>値段</td></tr>
	<tr bgcolor=#ffff66><td colspan=5>▼武器</td></tr>
	$syo_buki
	<tr><td colspan=5><div align="center"><input type=submit value=" 購入 "></div></td></tr>
	<tr bgcolor=#ffff66><td colspan=5>▼防具</td></tr>
	$syo_bougu
	<tr><td colspan=5><div align="center"><input type=submit value=" 購入 "></div></td></tr>
	<tr bgcolor=#ffff66><td colspan=5>▼魔法</td></tr>
	$syo_mahousyo
	<tr><td colspan=5><div align="center"><input type=submit value=" 購入 "></div></td></tr>
	<tr bgcolor=#ffff66><td colspan=5>▼御守</td></tr>
	$syo_omamori
	<tr><td colspan=5><div align="center"><input type=submit value=" 購入 "></div></td></form></tr>
	</table>
EOM
	&hooter("login_view","街に戻る");
exit;
}

sub buy{
    if(!$in{'syo_name'}){&error("商品を選びなはれ");}
    
	open(IN,"$syohin_file") || &error("Open Error : $syohin_file");
	eval{ flock (IN, 2); };
	@syohin_data=<IN>;
	close(IN);
	
	foreach(@syohin_data){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_nedan,$syo_kaisuu)=split(/<>/);
	     if($in{'syo_name'} eq $syo_name){
	         $syo_flag=1;
	         last;
	     }
	}
	if(!$syo_flag){&error("残念やな<br>そんな商品ないらしいで");}
	
	if($money <= $syo_nedan){&error("お金が足りな～い！");}
	$money-=$syo_nedan;
#データ更新
	open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);
	
	     if($in{'syo_name'} eq $buki_name or $in{'syo_name'} eq $bougu_name or $in{'syo_name'} eq $mahou_name or $in{'syo_name'} eq $omamori_name){&error("既に持ってる商品は買えへんで～");}
	foreach(@my_item_list){
	    &syouhin_sprit ($_);
	    if($in{'syo_name'} eq $syo_hinmoku){&error("既に持ってる商品は買えへんで～");}
	}
	unshift (@my_item_list,"$syo_syu<>$syo_name<>$syo_iryoku<>$syo_meityu<>$syo_kaisuu<>1<>0<>\n");
	
	open(OUT,">./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @my_item_list;
	close(OUT);
			
	&header(gym_style);
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$in{'syo_name'}を保管しました。
</span>
</td></tr></table>
<br>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>

	<form method=POST action="hanbai.cgi">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>hanbai<>">
	<input type=submit value="店に戻る">
	</form>
	</div>

	</body></html>
EOM
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);

exit;
}

sub soubi{
	open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);
	
	foreach(@my_item_list){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_kaisuu,$syo_lv,$syo_keiken)=split(/<>/);
	     if($syo_syu eq "武器"){
	     	     $syo_buki .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }elsif($syo_syu eq "防具"){
	     	     $syo_bougu .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }elsif($syo_syu eq "魔法"){
	     	     $syo_mahousyo .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }elsif($syo_syu eq "御守"){
	     	     $syo_omamori .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }
	}
	
    ($buki_iryoku,$buki_meityu,$buki_kaisuu,$buki_lv,$buki_keiken)=split(/\//,$buki);
    ($bougu_iryoku,$bougu_meityu,$bougu_kaisuu,$bougu_lv,$bougu_keiken)=split(/\//,$bougu);
    ($mahou_iryoku,$mahou_meityu,$mahou_kaisuu,$mahou_lv,$mahou_keiken)=split(/\//,$mahou);
    ($omamori_iryoku,$omamori_meityu,$omamori_kaisuu,$omamori_lv,$omamori_keiken)=split(/\//,$omamori);
    
	&header(gym_style);
	print <<"EOM";
	<table border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td>
	<table><form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>hanbai<>">
	<tr><td colspan=5><center><input type="submit" value="販売店へ行く"></center></td></tr>
	</form></table>
	</td><td>
	<table><form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>kajiya<>">
	<tr><td colspan=5><center><input type="submit" value="鍛冶屋へ行く"></center></td></tr>
	</form></table>
	</td></tr>
	</table>
	<br>
	<table border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>soubi_do<>">
	<tr bgcolor=#ccff33><td align=center nowrap>商品名</td><td align=center nowrap>威力</td><td>命中率（％）</td><td>使用可\能\回\数</td><td>レベル</td><td>経験地</td></tr>
	<tr bgcolor=#ffff66><td colspan=6>▼武器</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left>$buki_name</td><td>$buki_iryoku</td><td>$buki_meityu</td><td>$buki_kaisuu</td><td>$buki_lv</td><td>$buki_keiken</td></tr>
	$syo_buki
	<tr bgcolor=#ffff66><td colspan=6>▼防具</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left>$bougu_name</td><td>$bougu_iryoku</td><td>$bougu_meityu</td><td>$bougu_kaisuu</td><td>$bougu_lv</td><td>$bougu_keiken</td></tr>
	$syo_bougu
	<tr bgcolor=#ffff66><td colspan=6>▼魔法</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left>$mahou_name</td><td>$mahou_iryoku</td><td>$mahou_meityu</td><td>$mahou_kaisuu</td><td>$mahou_lv</td><td>$mahou_keiken</td></tr>
	$syo_mahousyo
	<tr bgcolor=#ffff66><td colspan=6>▼御守</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left>$omamori_name</td><td>$omamori_iryoku</td><td>$omamori_meityu</td><td>$omamori_kaisuu</td><td>$omamori_lv</td><td>$omamori_keiken</td></tr>
	$syo_omamori
	<tr><td colspan=6><div align="center">
	<select name="command">
	<option value="soubi">装備</option>
	<option value="baikyaku">売却</option>
	</select><input type=submit value=" 実行 "></div></td></form></tr>
	</table>
	<br>
EOM
	&hooter("login_view","街に戻る");
	
exit;
}

sub soubi_do{
    if(!$in{'syo_name'}){&error("商品を選びなはれ");}
    if($in{'command'} eq "baikyaku"){
        &soubi_uru;
        exit;
    }
    
	open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);
	
	foreach(@my_item_list){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_kaisuu,$syo_lv,$syo_keiken)=split(/<>/);
	     if($in{'syo_name'} eq $syo_name){
	         $syo_flag=1;
	         last;
	     }
	}
	if(!$syo_flag){&error("残念やな。そんなもんないらしいで");}
#データ更新

	     if($syo_syu eq "武器"){
             ($buki_iryoku,$buki_meityu,$buki_kaisuu,$buki_lv,$buki_keiken)=split(/\//,$buki);
             if($buki_name ne "素手"){
                 $mae_soubi="武器<>$buki_name<>$buki_iryoku<>$buki_meityu<>$buki_kaisuu<>$buki_lv<>$buki_keiken<>\n";
             }
	         $buki_name=$syo_name;
	         $buki="$syo_iryoku/$syo_meityu/$syo_kaisuu/$syo_lv/$syo_keiken/";
	     }elsif($syo_syu eq "防具"){
             ($bougu_iryoku,$bougu_meityu,$bougu_kaisuu,$bougu_lv,$bougu_keiken)=split(/\//,$bougu);
             if($bougu_name ne "洋服"){
                 $mae_soubi="防具<>$bougu_name<>$bougu_iryoku<>$bougu_meityu<>$bougu_kaisuu<>$bougu_lv<>$bougu_keiken<>\n";
             }
	         $bougu_name=$syo_name;
	         $bougu="$syo_iryoku/$syo_meityu/$syo_kaisuu/$syo_lv/$syo_keiken/";
	     }elsif($syo_syu eq "魔法"){
             ($mahou_iryoku,$mahou_meityu,$mahou_kaisuu,$mahou_lv,$mahou_keiken)=split(/\//,$mahou);
             if($mahou_name ne "念力"){
                 $mae_soubi="魔法<>$mahou_name<>$mahou_iryoku<>$mahou_meityu<>$mahou_kaisuu<>$mahou_lv<>$mahou_keiken<>\n";
             }
	         $mahou_name=$syo_name;
	         $mahou="$syo_iryoku/$syo_meityu/$syo_kaisuu/$syo_lv/$syo_keiken/";
	     }elsif($syo_syu eq "御守"){
             ($omamori_iryoku,$omamori_meityu,$omamori_kaisuu,$omamori_lv,$omamori_keiken)=split(/\//,$omamori);
             if($omamori_name ne "先祖の霊"){
                 $mae_soubi="御守<>$omamori_name<>$omamori_iryoku<>$omamori_meityu<>$omamori_kaisuu<>$omamori_lv<>$omamori_keiken<>\n";
             }
	         $omamori_name=$syo_name;
	         $omamori="$syo_iryoku/$syo_meityu/$syo_kaisuu/$syo_lv/$syo_keiken/";
	     }
	     
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			
	foreach(@my_item_list){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_kaisuu,$syo_lv,$syo_keiken)=split(/<>/);
	     if($in{'syo_name'} eq $syo_name){next;}
	     push (@new_item_list,$_);
	}
	unshift (@new_item_list,$mae_soubi);
	
	open(OUT,">./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @new_item_list;
	close(OUT);
			
	&header(gym_style);
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$in{'syo_name'}を装備しました。
</span>
</td></tr></table>
<br>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>

	<form method=POST action="hanbai.cgi">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>soubi<>">
	<input type=submit value="倉庫に戻る">
	</form>
	</div>

	</body></html>
EOM
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);

exit;
}

sub soubi_uru{
	open(IN,"$syohin_file") || &error("Open Error : $syohin_file");
	eval{ flock (IN, 2); };
	@syohin_data=<IN>;
	close(IN);
	
	foreach(@syohin_data){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_nedan,$syo_kaisuu)=split(/<>/);
	     if($in{'syo_name'} eq $syo_name){
	         if($in{'syo_name'} eq "素手" or $in{'syo_name'} eq "洋服" or $in{'syo_name'} eq "念力" or $in{'syo_name'} eq "先祖の霊"){
	             $baikyakuti=0;
	         }else{
	             $baikyakuti=$syo_nedan/10;
	             last;
	         }
	     }
	}

	open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);
	
	foreach(@my_item_list){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_kaisuu,$syo_lv,$syo_keiken)=split(/<>/);
	     if($in{'syo_name'} eq $syo_name){
	         $baikyakuti*=$syo_lv;
	         $money+=$baikyakuti;
	         $syo_flag=1;
	         next;
	     }
	     push (@new_item_list,$_);
	}
	if(!$syo_flag){&error("残念やな。そんなもんないらしいで");}

	open(OUT,">./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @new_item_list;
	close(OUT);
			
	&header(gym_style);
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$in{'syo_name'}を売却しました。<br>
    $baikyakuti円をＧＥＴしました。<br>
</span>
</td></tr></table>
<br>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>

	<form method=POST action="hanbai.cgi">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>soubi<>">
	<input type=submit value="倉庫に戻る">
	</form>
	</div>

	</body></html>
EOM
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);

exit;
}

sub kajiya{
	open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);
	
	foreach(@my_item_list){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_kaisuu,$syo_lv,$syo_keiken)=split(/<>/);
	     if($syo_syu eq "武器"){
	     	     $syo_buki .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }elsif($syo_syu eq "防具"){
	     	     $syo_bougu .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }elsif($syo_syu eq "魔法"){
	     	     $syo_mahousyo .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }elsif($syo_syu eq "御守"){
	     	     $syo_omamori .= "<tr bgcolor=#ccff99 align=center><td nowrap align=left><input type=\"radio\" name=\"syo_name\" value=\"$syo_name\">$syo_name</td><td>$syo_iryoku</td><td>$syo_meityu</td><td>$syo_kaisuu</td><td>$syo_lv</td><td>$syo_keiken</td></tr>";
	     }
	}
	
    ($buki_iryoku,$buki_meityu,$buki_kaisuu,$buki_lv,$buki_keiken)=split(/\//,$buki);
    ($bougu_iryoku,$bougu_meityu,$bougu_kaisuu,$bougu_lv,$bougu_keiken)=split(/\//,$bougu);
    ($mahou_iryoku,$mahou_meityu,$mahou_kaisuu,$mahou_lv,$mahou_keiken)=split(/\//,$mahou);
    ($omamori_iryoku,$omamori_meityu,$omamori_kaisuu,$omamori_lv,$omamori_keiken)=split(/\//,$omamori);
    
	&header(gym_style);
	print <<"EOM";
	<table border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td>
	<table><form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>soubi<>">
	<tr><td colspan=5><center><input type="submit" value="倉庫へ行く"></center></td></tr>
	</form></table>
	</td><td>
	<table><form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>hanbai<>">
	<tr><td colspan=5><center><input type="submit" value="販売店へ行く"></center></td></tr>
	</form></table>
	</td></tr>
	</table>
	<br>
	<table border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<form method="POST" action="$this_script">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>kajiya_do<>">
	<tr bgcolor=#ccff33><td align=center nowrap>商品名</td><td align=center nowrap>威力</td><td>命中率（％）</td><td>使用可\能\回\数</td><td>レベル</td><td>経験地</td></tr>
	<tr bgcolor=#ffff66><td colspan=6>▼武器</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left><input type="radio" name="syo_name" value="$buki_name">$buki_name</td><td>$buki_iryoku</td><td>$buki_meityu</td><td>$buki_kaisuu</td><td>$buki_lv</td><td>$buki_keiken</td></tr>
	$syo_buki
	<tr bgcolor=#ffff66><td colspan=6>▼防具</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left><input type="radio" name="syo_name" value="$bougu_name">$bougu_name</td><td>$bougu_iryoku</td><td>$bougu_meityu</td><td>$bougu_kaisuu</td><td>$bougu_lv</td><td>$bougu_keiken</td></tr>
	$syo_bougu
	<tr bgcolor=#ffff66><td colspan=6>▼魔法</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left><input type="radio" name="syo_name" value="$mahou_name">$mahou_name</td><td>$mahou_iryoku</td><td>$mahou_meityu</td><td>$mahou_kaisuu</td><td>$mahou_lv</td><td>$mahou_keiken</td></tr>
	$syo_mahousyo
	<tr bgcolor=#ffff66><td colspan=6>▼御守</td></tr>
	<tr bgcolor=#00ff00 align=center><td nowrap align=left><input type="radio" name="syo_name" value="$omamori_name">$omamori_name</td><td>$omamori_iryoku</td><td>$omamori_meityu</td><td>$omamori_kaisuu</td><td>$omamori_lv</td><td>$omamori_keiken</td></tr>
	$syo_omamori
	<tr><td colspan=6><div align="center">
	耐久力を
	<select name="taikyuu_up">
	<option value="" selected>upしない</option>
	<option value="1">１up</option>
	<option value="3">３up</option>
	<option value="5">５up</option>
	<option value="10">１０up</option>
	<option value="15">１５up</option>
	<option value="25">２５up</option>
	<option value="50">５０up</option>
	</select>
	威力を
	<select name="iryoku_up">
	<option value="" selected>upしない</option>
	<option value="1">１up</option>
	<option value="3">３up</option>
	<option value="5">５up</option>
	<option value="10">１０up</option>
	<option value="15">１５up</option>
	<option value="25">２５up</option>
	<option value="50">５０up</option>
	</select>
	<input type=submit value=" 実行 "></div></td></form></tr>
	</table>
	<br>
EOM
	&hooter("login_view","街に戻る");
	
	exit;
}

sub kajiya_do{
    if(!$in{'syo_name'}){&error("商品を選びなはれ");}
    if(!$in{'iryoku_up'} and !$in{'taikyuu_up'}){&error("なんか実行しようよ");}
    if($in{'iryoku_up'}){
        $comment .= "  威力を$in{'iryoku_up'}  ";
    }
    if($in{'taikyuu_up'}){
        $comment .= "  耐久力を$in{'taikyuu_up'}  ";
    }
    $hiyou=$in{'iryoku_up'}*10000 + $in{'taikyuu_up'}*1000;
    if($hiyou>$money){&error("お金が足りへんで");}
    $money-=$hiyou;
    
	if($in{'syo_name'} eq $buki_name){
        ($buki_iryoku,$buki_meityu,$buki_kaisuu,$buki_lv,$buki_keiken)=split(/\//,$buki);
        $buki_iryoku += $in{'iryoku_up'};
        $buki_kaisuu += $in{'taikyuu_up'};
        $buki="$buki_iryoku/$buki_meityu/$buki_kaisuu/$buki_lv/$buki_keiken/";
	}elsif($in{'syo_name'} eq $bougu_name){
        ($bougu_iryoku,$bougu_meityu,$bougu_kaisuu,$bougu_lv,$bougu_keiken)=split(/\//,$bougu);
        $bougu_iryoku += $in{'iryoku_up'};
        $bougu_kaisuu += $in{'taikyuu_up'};
        $bougu="$bougu_iryoku/$bougu_meityu/$bougu_kaisuu/$bougu_lv/$bougu_keiken/";
	}elsif($in{'syo_name'} eq $mahou_name){
        ($mahou_iryoku,$mahou_meityu,$mahou_kaisuu,$mahou_lv,$mahou_keiken)=split(/\//,$mahou);
        $mahou_iryoku += $in{'iryoku_up'};
        $mahou_kaisuu += $in{'taikyuu_up'};
        $mahou="$mahou_iryoku/$mahou_meityu/$mahou_kaisuu/$mahou_lv/$mahou_keiken/";
	}elsif($in{'syo_name'} eq $omamori_name){
        ($omamori_iryoku,$omamori_meityu,$omamori_kaisuu,$omamori_lv,$omamori_keiken)=split(/\//,$omamori);
        $omamori_iryoku += $in{'iryoku_up'};
        $omamori_kaisuu += $in{'taikyuu_up'};
        $omamori="$omamori_iryoku/$omamori_meityu/$omamori_kaisuu/$omamori_lv/$omamori_keiken/";
	}else{
	    $moti_flag="off";
	}
	
	open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);
	
	foreach(@my_item_list){
	     ($syo_syu,$syo_name,$syo_iryoku,$syo_meityu,$syo_kaisuu,$syo_lv,$syo_keiken)=split(/<>/);
	     if($syo_syu eq "武器" or $syo_syu eq "防具" or $syo_syu eq "魔法" or $syo_syu eq "御守"){
	         if($in{'syo_name'} eq $syo_name){
	             $syo_flag=1;
	             $syo_iryoku += $in{'iryoku_up'};
	             $syo_kaisuu += $in{'taikyuu_up'};
	         }
	         push (@new_item_list,"$syo_syu<>$syo_name<>$syo_iryoku<>$syo_meityu<>$syo_kaisuu<>$syo_lv<>$syo_keiken<>\n");
	     }else{
	         push (@new_item_list,$_);
	     }
	}
	if(!$syo_flag and $moti_flag eq "off"){&error("残念やな。そんなもんないらしいで");}
	
	open(OUT,">./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @new_item_list;
	close(OUT);
	
	&header(gym_style);
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$in{'syo_name'}の$commentあげました。<br>
    $hiyou円を支払いました。<br>
</span>
</td></tr></table>
<br>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>

	<form method=POST action="hanbai.cgi">
	<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$in{'k_id'}<>$in{'town_no'}<>kajiya<>">
	<input type=submit value="鍛冶屋に戻る">
	</form>
	</div>

	</body></html>
EOM
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
exit;
}