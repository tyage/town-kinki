#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
#
#  オリジナル　「ゆかにゃん」さん
#　改造 Edit:たっちゃん　2005/12/03
################################# unit.pl ####################
#"アイテム" => "<form method=POST action=\"item.cgi\"><input type=hidden name=mode value=\"item_make\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/img062.gif'  onMouseOver='onMes5(\"アイテムのアイデア紹介・登録。\")' onMouseOut='onMes5(\"\")'></td></form>\n",
##############################################################
require './town_ini.cgi';
require './town_lib.pl';
&decode;

################　いろいろ設定　###############

# このファイル名
$this_script = 'item.cgi';

# 管理者のみ許可
$kanrsyanomi = 'no'; #'yes';

# 書込アイテムの検査をする。
$kensa = 'yes'; # ('yes' = する)('no' = しない)

# 問屋の数を増やす。
$tonya0 = './dat_dir/syouhin.cgi';# './dat_dir/syouhin.cgi'; #koko2006/12/10追加
$tonya1 = './dat_dir/otakara.cgi';# './dat_dir/otakara.cgi';
$tonya2 = './dat_dir/gousei.cgi';
$tonya3 = './dat_dir/jihanki.cgi';
$tonya4 = './dat_dir/keihin.cgi';
$tonya5 = './dat_dir/prezento.cgi';

#特殊アイテム種類追加「宝箱用」#2006/11/20
@item_otakara_sybetu = ("スペシャル","金の箱","銀の箱","銅の箱","デパート");
#アイテム種類設定（すべては変更しないでください）#koko2005/12/03
@item_make_syubetu = (@global_syouhin_syubetu,@item_otakara_sybetu);
## @item_make_syubetu = ("すべて","スーパー","書籍","食料品","薬","スポーツ用品","電化製品","美容","アダルト","DVD","ファーストフード","日用品","お花","デザート","ギフト","泡盛･アルコール","乗り物","ゲーム");#ここは元ファイルを使うtown_ini

#アイテム効果
@kouka = ("無","万能\","風邪","肺炎","結核","ウエイトアップ","ダイエット","身長","縮み","クレジット");
#アイテム属性「ファーストフード」は「ー」がエラーのため「ファ」になります。
@zokusei = ("無","ギフト","食料品","ファ","ステータス");

#アイテム桁数
$item_ketasu = 2;
#値段桁数
$nedan_ketasu =10;

#アイテム新規投稿用基本データ
$new_item="<><>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>回<>0<>5<>0<>0<>0<>0<><>0<>0<>0<>";

#アイテム効果の説明
$kouka_set="ウエイトアップ、ダイエット、身長（が伸びます）、（身長が）縮みは
<BR>数値入力でそれぞれ○.○ｃｍ、○.○ｋｇになります
<BR>万能\はすべての病気に効果が
<BR>風邪、肺炎、結核はそれぞれの病気の治療に効果があります
<BR>数値は少し効果が5、効果が10、大きな効果が20を目安に
";

#アイテム投稿ファイル（書き込み可能パーミッションにしてサーバーにアップしてください）
$toukou_file='./log_dir/item_toukou.cgi';
#注意事項
$can="
投稿したアイテムの修正は投稿者、ゲーム管理者のみできます<BR>
注意事項はここに表\示されます
";
####################　注意　################################
# unit.pl
# "アイテム" => "<form method=POST action=\"item.cgi\"><input type=hidden name=mode value=\"item_make\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/img062.gif'  onMouseOver='onMes5(\"アイテムのアイデア紹介・登録。\")' onMouseOut='onMes5(\"\")'></td></form>\n",

# 作成　log_dir/item_toukou.cgi
# アイテム投稿記録上限　koko2005/12/06
$item_max = 150;
###########################################################

#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
	
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}

#koko2005/12/03
	if ($in{'ty0'}){$in{'ty'} = $in{'ty0'};}
	if ($in{'item_ty0'}){$in{'item_ty'} = $in{'item_ty0'};}
#	if ($in{'syo_zaiko'}){$in{'syo_zaiko'} *= $zaiko_tyousetuti;}
#kokoend
#koko207/05/05
#	if ($in{'name'} eq 'たっちゃん'){
#		$toukou_file='./dat_dir/syouhin.cgi';
#		$item_max = 500;
#	}
#kokoend
#条件分岐

	if($in{'mode'} eq "item_make"){&item_make;}
	elsif($in{'mode'} eq "item_make1"){&item_make1;}
	elsif($in{'mode'} eq "item_make_w1"){&item_make_w1;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

#######アイテム作成
sub item_make{
	&header(syokudou_style);
	if($toukou_file){
		@item_all =();
		$item_file="$toukou_file";
		open(OL,"< $item_file") || &error("Open Error : $toukou_file");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
		$x2=@item_all;
		$t_ty="new";
#koko2006/12/02
	}
#koko2006/12/10

	if($tonya0){
		@item_all0 =();
		open(OL,"< $tonya0") || &error("Open Error : $tonya0");
		eval{ flock (OL, 1); };
		@item_all0 = <OL>;
		close(OL);
		$t_ty="moto";

	}
#kokoend
	if($tonya1){
		@item_all1 = ();
		open(OL,"< $tonya1") || &error("Open Error : $tonya1");
		eval{ flock (OL, 1); };
		@item_all1 = <OL>;
		close(OL);
		$t_ty="moto";

	}
	if($tonya2){
		@item_all2 =();
		open(OL,"< $tonya2") || &error("Open Error : $tonya2");
		eval{ flock (OL, 1); };
		@item_all2 = <OL>;
		close(OL);
		$t_ty="moto";

	}
	if($tonya3){
		@item_all3 =();
		open(OL,"< $tonya3") || &error("Open Error : $tonya3");
		eval{ flock (OL, 1); };
		@item_all3 = <OL>;
		close(OL);
		$t_ty="moto";

	}
	if($tonya4){
		@item_all4 =();
		open(OL,"< $tonya4") || &error("Open Error : $tonya4");
		eval{ flock (OL, 1); };
		@item_all4 = <OL>;
		close(OL);
		$t_ty="moto";

	}
	if($tonya5){
		@item_all5 =();
		open(OL,"< $tonya5") || &error("Open Error : $tonya5");
		eval{ flock (OL, 1); };
		@item_all5 = <OL>;
		close(OL);
		$t_ty="moto";
	}
	@item_all =();
	$item_file=$toukou_file;
	open(OL,"< $item_file") || &error("Open Error : $toukou_file");
	eval{ flock (OL, 1); };
	@item_all = <OL>;
	close(OL);
	$t_ty="moto";
#kokoend
#koko2006/04/22
	$i = 0;
	foreach (@item_all){
		++$i;
		(@cheku_item) = split(/<>/);
		if ($#cheku_item != 33 && $kensa eq 'yes'){&error("アイテムエラー:$toukou_file：$cheku_item[0],$cheku_item[1] 数 $#cheku_item $i行目");}
#koko2006/12/02
		$aru_itm = 0;
		foreach (@item_make_syubetu){
			if ($cheku_item[0] eq $_){
				$aru_itm = 1;
				last;
			}
		}
		if ($aru_itm == 0){
			push @item_make_syubetu,$cheku_item[0];
		}
	}
	if (@item_all0){
		$i =0;
		foreach (@item_all0){
			++$i;
			(@cheku_item) = split(/<>/);
			if ($#cheku_item != 33 && $kensa eq 'yes'){&error("アイテムエラー0:$tonya0：$cheku_item[0],$cheku_item[1] 数 $#cheku_item $i行目");}
			$aru_itm = 0;
			if($cheku_item[0] eq '種類'){next;}
			foreach (@item_make_syubetu0){
				if ($cheku_item[0] eq $_){
					$aru_itm = 1;
					last;
				}
			}
			if ($aru_itm == 0){
				push @item_make_syubetu0,$cheku_item[0];
				$log_syubetu0 .="<option value=$cheku_item[0]>$cheku_item[0]</option>\n";

			}
		}
	}

	if (@item_all1){
		$i =0;
		foreach (@item_all1){
			++$i;
			(@cheku_item) = split(/<>/);
			if ($#cheku_item != 33 && $kensa eq 'yes'){&error("アイテムエラー2:$tonya1：$cheku_item[0],$cheku_item[1] 数 $#cheku_item $i行目");}
			$aru_itm = 0;
			if($cheku_item[0] eq '種類'){next;}
			foreach (@item_make_syubetu1){
				if ($cheku_item[0] eq $_){
					$aru_itm = 1;
					last;
				}
			}
			if ($aru_itm == 0){
				push @item_make_syubetu1,$cheku_item[0];
				$log_syubetu1 .="<option value=$cheku_item[0]>$cheku_item[0]</option>\n";

			}
		}
	}

	if (@item_all2){
		$i =0;
		foreach (@item_all2){
			++$i;
			(@cheku_item) = split(/<>/);
			if ($#cheku_item != 33 && $kensa eq 'yes'){&error("アイテムエラー3：$tonya2:$cheku_item[0],$cheku_item[1] 数 $#cheku_item $i行目");}
			$aru_itm = 0;
			if($cheku_item[0] eq '種類'){next;}
			foreach (@item_make_syubetu2){
				if ($cheku_item[0] eq $_){
					$aru_itm = 1;
					last;
				}
			}
			if ($aru_itm == 0){
				push @item_make_syubetu2,$cheku_item[0];
				$log_syubetu2 .="<option value=$cheku_item[0]>$cheku_item[0]</option>\n";

			}
		}
	}

	if (@item_all3){
		$i =0;
		foreach (@item_all3){
			++$i;
			(@cheku_item) = split(/<>/);
			if ($#cheku_item != 33 && $kensa eq 'yes'){&error("アイテムエラー4：$tonya3:$cheku_item[0],$cheku_item[1] 数 $#cheku_item $i行目");}
			$aru_itm = 0;
			if($cheku_item[0] eq '種類'){next;}
			foreach (@item_make_syubetu3){
				if ($cheku_item[0] eq $_){
					$aru_itm = 1;
					last;
				}
			}
			if ($aru_itm == 0){
				push @item_make_syubetu3,$cheku_item[0];
				$log_syubetu3 .="<option value=$cheku_item[0]>$cheku_item[0]</option>\n";

			}
		}
	}

	if (@item_all4){
		$i =0;
		foreach (@item_all4){
			++$i;
			(@cheku_item) = split(/<>/);
			if ($#cheku_item != 33 && $kensa eq 'yes'){&error("アイテムエラー5：$tonya4:$cheku_item[0],$cheku_item[1] 数 $#cheku_item $i行目");}
			$aru_itm = 0;
			if($cheku_item[0] eq '種類'){next;}
			foreach (@item_make_syubetu4){
				if ($cheku_item[0] eq $_){
					$aru_itm = 1;
					last;
				}
			}
			if ($aru_itm == 0){
				push @item_make_syubetu4,$cheku_item[0];
				$log_syubetu4 .="<option value=$cheku_item[0]>$cheku_item[0]</option>\n";

			}
		}
	}

	if (@item_all5){
		$i =0;
		foreach (@item_all5){
			++$i;
			(@cheku_item) = split(/<>/);
			if ($#cheku_item != 33 && $kensa eq 'yes'){&error("アイテムエラー6：$tonya5:$cheku_item[0],$cheku_item[1] 数 $#cheku_item $i行目");}
			$aru_itm = 0;
			if($cheku_item[0] eq '種類'){next;}
			foreach (@item_make_syubetu5){
				if ($cheku_item[0] eq $_){
					$aru_itm = 1;
					last;
				}
			}
			if ($aru_itm == 0){
				push @item_make_syubetu5,$cheku_item[0];
				$log_syubetu5 .="<option value=$cheku_item[0]>$cheku_item[0]</option>\n";

			}
		}
	}

#kokoend
	if($x2 eq ""){$x2=0;}
	foreach (@item_make_syubetu){
#		if ($_ eq "すべて"){next;}#koko2005/12/03
		$log_syubetu .= "<option value=$_>$_</option>\n";
	}
	 print <<"EOM";
	<table border="0" cellspacing="0" cellpadding="10" align="center" class="yosumi">
	<td bgcolor="#ffffff">
	<center>
	表\示する内容を選んでください<BR><BR>
	<table>
	<TD>投稿されている
	<form method="POST" action="$this_script">
	<input type="hidden" name="mode" value="item_make">
	<input type=hidden name=tonya value="tonya">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="new">
	<input type="hidden" name="toroku" value="toroku">
	<TD><select name="item_ty">
	<option value="すべて">すべて</option><!--koko2005/12/05-->
	$log_syubetu
	<option value="">表\示しない</option>\n
	</select>
	<TD>
	<input type="submit" value="表\示する">
	</TD></form>
	<TR>
	<td colspan=3>現在$x2の投稿があります
	<TR>
	<td colspan=3><HR>
	<TR>
	<TD><BR>現在ある
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item_make">
	<input type=hidden name=tonya value="tonya0">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="moto">
	<TD><BR><select name="item_ty">
	$log_syubetu0
	<option value="">表\示しない</option>
	</select>
	<TD><BR>
	<input type="submit" value="表\示する">
	</TD></form>
EOM
	if ($kanrsyanomi ne 'yes' || "$name" eq "$admin_name"){
		print <<"EOM";
	<TR><TD><BR>現在ある
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item_make">
	<input type=hidden name=tonya value="tonya1">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="moto">
	<TD><BR><select name="item_ty">
	$log_syubetu1
	<option value="">表\示しない</option>
	</select>
	<TD><BR>
	<input type="submit" value="表\示する">
	</TD></form></TR>

	<TR><TD><BR>現在ある
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item_make">
	<input type=hidden name=tonya value="tonya2">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="moto">
	<TD><BR><select name="item_ty">
	$log_syubetu2
	<option value="">表\示しない</option>
	</select>
	<TD><BR>
	<input type="submit" value="表\示する">
	</TD></form></TR>

	<TR><TD><BR>現在ある
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item_make">
	<input type=hidden name=tonya value="tonya3">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="moto">
	<TD><BR><select name="item_ty">
	$log_syubetu3
	<option value="">表\示しない</option>
	</select>
	<TD><BR>
	<input type="submit" value="表\示する">
	</TD></form></TR>

	<TR><TD><BR>現在ある
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item_make">
	<input type=hidden name=tonya value="tonya4">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="moto">
	<TD><BR><select name="item_ty">
	$log_syubetu4
	<option value="">表\示しない</option>
	</select>
	<TD><BR>
	<input type="submit" value="表\示する">
	</TD></form></TR>

	<TR><TD><BR>現在ある
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item_make">
	<input type=hidden name=tonya value="tonya5">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="moto">
	<TD><BR><select name="item_ty">
	$log_syubetu5
	<option value="">表\示しない</option>
	</select>
	<TD><BR>
	<input type="submit" value="表\示する">
	</TD></form></TR>
EOM
	}
	print <<"EOM";
	</table><HR>
	</center>
	$can
	<center>
	<HR>
		<form method="POST" action="$script">
		<input type="hidden" name="mode" value="login_view">
		<input type="hidden" name="name" value="$in{'name'}">
		<input type="hidden" name="pass" value="$in{'pass'}">
		<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
		<input type="hidden" name="town_no" value="$in{'town_no'}">
		<input type="submit" value="戻る">
		</form>
	</tr></table><br>
		<form method="POST" action="$this_script">
	<input type="hidden" name="mode" value="item_make1">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="item_ty" value="$in{'item_ty'}">
	<input type="hidden" name="t_ty" value="$t_ty">
EOM
print"<table width=\"100%\" border=\"0\" cellspacing=\"1\" cellpadding=\"5\" align=\"center\" class=\"yosumi\">";
	
	if($in{'item_ty'} ne ""){
#koko2006/12/02
		if($in{'tonya'} eq "tonya0"){@item_all = @item_all0;}
		if($in{'tonya'} eq "tonya1"){@item_all = @item_all1;}
		if($in{'tonya'} eq "tonya2"){@item_all = @item_all2;}
		if($in{'tonya'} eq "tonya3"){@item_all = @item_all3;}
		if($in{'tonya'} eq "tonya4"){@item_all = @item_all4;}
		if($in{'tonya'} eq "tonya5"){@item_all = @item_all5;}
#kokoend
		$xx=0;
		foreach (@item_all){
			$hyuuji=0;
			&syouhin_sprit($_);
			if($syo_syubetu eq $in{'item_ty'} || ($in{'item_ty'}eq "すべて" && $in{'toroku'} eq 'toroku')){ #koko2005/12/03
				if($in{'t_ty'} eq "moto"){
					if($xx!=0){$hyuuji=1;}
				}else{
					$hyuuji=1;
				}
			}
			if($hyuuji==1){
				if($in{'t_ty'} eq "new"){
					if("$syo_kounyuubi" eq "$name" || "$name" eq "$admin_name"){
						$toukou_sl ="<input type=\"radio\" value=\"$xx\" name=\"syo_hinmoku\">";
						$toukou_flag = 1;
					}else{
						$toukou_sl="";
					}
					$darekana="投稿者：$syo_kounyuubi<BR>";
				}else{
					$toukou_sl ="<input type=\"radio\" value=\"$xx\" name=\"syo_hinmoku\">";
					$toukou_flag = 1;
					$darekana="";
				
				}
				if($syo_cal > 0){
					$calory_hyouzi = "$syo_cal kcal";
				}else{
					$calory_hyouzi = "ー";
				}
				if ($maeno_syo_syubetu ne "$syo_syubetu"){
					print <<"EOM";
				<tr><td colspan="26"><div align="center">
				<tr bgcolor="#ff9933"><td align="center" width="150">商品</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align="center" nowrap>カロリー</td><td align="center" nowrap>耐久</td><td align="center">使用<br>間隔</td><td align="center">身体<br>消費</td><td align="center">頭脳<br>消費</td><td align="center">価格</td><td align="center" nowrap>在庫</td></tr><!-- #koko2006/11/10 -->
				<tr bgcolor="#ffff66"><td colspan=26><font size="4">▼$syo_syubetu</font></td></tr>
EOM
				}
				$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
				if ($syo_nedan =~ /^[-+]?\d\d\d\d+/g){
 					for ($i = pos($syo_nedan) - 3, $j = $syo_nedan =~ /^[-+]/; $i > $j; $i -= 3){
    					substr($syo_nedan, $i, 0) = ',';
  					}
				}

#ver.1.3ここまで
#koko2006/11/10
	if ($syo_comment){
		$disp_seru = "rowspan=\"2\"";
		$disp_com = "<tr bgcolor=\"#cccccc\"><td align=left colspan=24>【 備考 】 $syo_comment</td></tr>";
	}else{
		$disp_seru = "";
		$disp_com = "";
	}

			print <<"EOM";
	<tr bgcolor="#ffcc66" align="center"><td align="left" nowrap $disp_seru>$toukou_sl $syo_hinmoku\[$xx\]</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align="right" nowrap>$calory_hyouzi</td><td nowrap>$taikyuu_hyouzi_seikei</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td align="right" nowrap>$syo_nedan円</td><td align="right">$syo_zaiko</td></tr>$disp_com<tr bgcolor="#ffff66"><td colspan=26>
$darekana
効果：$syo_kouka<BR>
</td></tr>
EOM
#kokoend
				$maeno_syo_syubetu = "$syo_syubetu";
			}
			$xx++;
		}
	}
#koko2007/12/08
	if($admin_name eq $in{'name'}){
		$fail_disp .= "<input type=checkbox name=delet value=\"delet\">削除 ";
		$fail_disp .= "<select name=fail>";
		if($tonya0){$fail_disp .= "<option value=$tonya0>$tonya0</option>\n";}
		if($tonya1){$fail_disp .= "<option value=$tonya1>$tonya1</option>\n";}
		if($tonya2){$fail_disp .= "<option value=$tonya2>$tonya2</option>\n";}
		if($tonya3){$fail_disp .= "<option value=$tonya3>$tonya3</option>\n";}
		if($tonya4){$fail_disp .= "<option value=$tonya4>$tonya4</option>\n";}
		if($tonya5){$fail_disp .= "<option value=$tonya5>$tonya5</option>\n";}
		$fail_disp .= "</select>に登録 \n";
		$fail_disp .= "<input type=checkbox name=fa value=\"tuika\">追加 ";
	}
#koko2006/12/10
	if ($toukou_flag == 1 && $in{'tonya'} eq 'tonya'&& !($admin_name eq $in{'name'})){
		$toukou_disp = "<input type=checkbox name=dele value=\"dele\">削除 ";
	}
	print"
	<tr><td colspan=26 align=center>
	<input type=hidden name=tonya value=\"$in{'tonya'}\">
	<input type=hidden name=x2 value=$x2>
	$toukou_disp $fail_disp
	<input type=submit value=\"修正／新規登録\">
	</form>
	</td></tr></table>";
#kokoend		
	print "<div align=\"right\">オリジナル:ゆかにゃん<br>Edit:たっちゃん<div>\n";
	print "</body></html>\n";
	exit;
}

#アイテム修正
sub item_make1{
#koko2007/12/08
	if($admin_name eq $in{'name'} && ($in{'delet'} || $in{'fa'}) && !$inshita){
		$inshita = 1;
		&make;
		&error("ＥＮＤエラー");
		exit;
	}
	# アイテム削除 #koko2006/12/10
	if ($in{'dele'} eq 'dele'){
		if($in{'syo_hinmoku'} ne ""){
			$item_file= $toukou_file; #koko2006/12/10
			open(OL,"< $item_file") || &error("Open Error : $toukou_file");
			eval{ flock (OL, 1); };
			@item_all = <OL>;
			close(OL);
			splice @item_all,$in{'syo_hinmoku'},1;
			open(OLOUT,">$item_file") || &error("$item_fileに書き込みが出来ません");
			eval{ flock (OLOUT, 2); };
			print OLOUT @item_all;
			close(OLOUT);
		}

		$in{'mode'}='item_make';
		$in{'t_ty'}='new';
		$in{'toroku'}='toroku';
		&item_make;
		exit;
	}
	#kokoend
	&header(syokudou_style);
	#koko2006/12/02	
	if($in{'t_ty'} eq "new" || $in{'syo_hinmoku'} eq ""){
		$item_file="$toukou_file";
		open(OL,"< $item_file") || &error("Open Error : $toukou_file");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya0"){
		$item_file=$tonya0;
		open(OL,"< $item_file") || &error("Open Error : $tonya1");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya1"){
		$item_file=$tonya1;
		open(OL,"< $item_file") || &error("Open Error : $tonya1");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya2"){
		$item_file=$tonya2;
		open(OL,"< $item_file") || &error("Open Error : $tonya2");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya3"){
		$item_file=$tonya3;
		open(OL,"< $item_file") || &error("Open Error : $tonya3");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya4"){
		$item_file=$tonya4;
		open(OL,"< $item_file") || &error("Open Error : $tonya4");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya5"){
		$item_file=$tonya5;
		open(OL,"< $item_file") || &error("Open Error : $tonya5");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'t_ty'} eq "moto"){
		$item_file= $toukou_file; #koko2006/12/10
		open(OL,"< $item_file") || &error("Open Error : $toukou_file");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}
	$x2=@item_all;
#kokoend
#koko2006/04/22
	foreach (@item_all){
		(@cheku_item) = split(/<>/);
		if ($#cheku_item != 33){&error("アイテムエラー2：$cheku_item[0],$cheku_item[1] 数 $#cheku_item");}
	}
#kokoend
	if ($in{'syo_hinmoku'} eq ""){
		&syouhin_sprit($new_item);
		$dou="new";
		$toukou_sl ="
		<td colspan=2>新規登録します
		";
	}elsif($in{'t_ty'} eq "new"){
		&syouhin_sprit($item_all[($in{'syo_hinmoku'})]);
		$toukou_sl ="
		<TD>アイテムＩＤ</td><td><input type=\"radio\" value=\"$in{'syo_hinmoku'}\" name=\"ss\" CHECKED>このデータを修正<Br>
		<input type=\"radio\" value=\"$in{'x2'}\" name=\"ss\">このデータを元に新規登録
		";
		$dou="naosi";
	}elsif($in{'t_ty'} eq "moto"){
		$moto_data=$item_all[($in{'syo_hinmoku'})];
		&syouhin_sprit($moto_data);
		$toukou_sl ="
		<td colspan=\"2\">このデータを元に新規登録
		";
		$dou="moto";
	}
		
	$syu="<select name=ty>";
	foreach (@item_make_syubetu){
		if($_ eq "すべて"){next;}
		
		$syu.="<option value=$_ ";
		if($syo_syubetu eq $_){
			$syu.="selected ";
			$syou_flag = "1";#koko2005/12/03
		}
		$syu.=">$_</option>\n";
		
		
	}
	
	$syu.="</select>";
	if($syo_kouka ne "無"){
	($koukahadou,$sonoiryoku,$jyanru) = split(/,/,$syo_kouka);
	}
#koko2006/10/16
	foreach (@zokusei){
		$zokusei_disp .= "<option value=\"$_\"";
		if($koukahadou eq $_ || $sonoiryoku eq $_ || $jyanru eq $_){
			$zokusei_disp .= " selected";
		}
		$zokusei_disp .= ">$_</option>\n";
	}
#kokoend
	if($syo_taikyuu_tani eq "回"){
		$taitai="
		<select name=tai>
		<option value=回 selected>回</option>
		<option value=日>日</option>
		";
	}else{
		$taitai="
		<select name=tai>
		<option value=回>回</option>
		<option value=日 selected>日</option>
		";
	}
	
	$kou1="<select name=kou1>";
	$kou2="<select name=kou2>";
	
	foreach (@kouka){
		$kou1.="<option value=$_ ";
		if($koukahadou eq $_){
			$kou1.="selected ";
			$syou_flag = "1";#koko2005/12/03
		}
		$kou1.=">$_</option>\n";
	}

	$kou1.="</select>";
	$syo_siyou_date=0;
	$tanka=0;
	$syo_kounyuubi=0;
	$tokubai=0;

	if(!$syou_flag){$disp_syo = $syo_syubetu;}#koko2005/12/03
#	$syo_zaiko /= $zaiko_tyousetuti;#koko2005/12/03

	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type="hidden" name="mode" value="item_make_w1">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="item_no" value="$in{'syo_hinmoku'}">
	<input type="hidden" name="item_ty" value="$in{'item_ty'}">
	<input type="hidden" name="dou" value="$dou">
<table border="1" cellspacing="1" cellpadding="5" align="center" class="yosumi">
$toukou_sl
<TR><TD>種類</td><td>$syu <input type="text" size="20" value="$disp_syo" name="ty0" maxlength="20"></td><!--koko2005/12/03-->
<TR><TD>品名</td><TD><input type="text" size="70" value="$syo_hinmoku" name="syo_hinmoku" maxlength="50"></TD></TR>
<TR><td>国語up値</td><TD><input type="text" size="2" value="$syo_kokugo" name="syo_kokugo" maxlength="$item_ketasu"></TD></TR>
<TR><td>数学up値</td><TD><input type="text" size="2" value="$syo_suugaku" name="syo_suugaku" maxlength="$item_ketasu"></TD></TR>
<TR><td>理科up値</td><TD><input type="text" size="2" value="$syo_rika" name="syo_rika" maxlength="$item_ketasu"></TD></TR>
<TR><td>社会up値</td><TD><input type="text" size="2" value="$syo_syakai" name="syo_syakai" maxlength="$item_ketasu"></TD></TR>
<TR><td>英語up値</td><TD><input type="text" size="2" value="$syo_eigo" name="syo_eigo" maxlength="$item_ketasu"></TD></TR>
<TR><td>音楽up値</td><TD><input type="text" size="2" value="$syo_ongaku" name="syo_ongaku" maxlength="$item_ketasu"></TD></TR>
<TR><td>美術up値</td><TD><input type="text" size="2" value="$syo_bijutu" name="syo_bijutu" maxlength="$item_ketasu"></TD></TR>
<TR><td>ルックスup値</td><TD><input type="text" size="2" value="$syo_looks" name="syo_looks" maxlength="$item_ketasu"></TD></TR>
<TR><td>体力up値</td><TD><input type="text" size="2" value="$syo_tairyoku" name="syo_tairyoku" maxlength="$item_ketasu"></TD></TR>
<TR><td>健康up値</td><TD><input type="text" size="2" value="$syo_kenkou" name="syo_kenkou" maxlength="$item_ketasu"></TD></TR>
<TR><td>スピードup値</td><TD><input type="text" size="2" value="$syo_speed" name="syo_speed" maxlength="$item_ketasu"></TD></TR>
<TR><td>パワーup値</td><TD><input type="text" size="2" value="$syo_power" name="syo_power" maxlength="$item_ketasu"></TD></TR>
<TR><td>腕力up値</td><TD><input type="text" size="2" value="$syo_wanryoku" name="syo_wanryoku" maxlength="$item_ketasu"></TD></TR>
<TR><td>脚力up値</td><TD><input type="text" size="2" value="$syo_kyakuryoku" name="syo_kyakuryoku" maxlength="$item_ketasu"></TD></TR>
<TR><td>LOVEup値</td><TD><input type=text size=2 value="$syo_love" name=syo_love maxlength="$item_ketasu"></TD></TR>
<TR><td>面白さup値</td><TD><input type="text" size="2" value="$syo_unique" name="syo_unique" maxlength="$item_ketasu"></TD></TR>
<TR><td>エッチup値</td><TD><input type="text" size="2" value="$syo_etti" name="syo_etti" maxlength="$item_ketasu"></TD></TR>

<TR><td>カロリー</td><TD><input type="text" size="4" value="$syo_cal" name="syo_cal" maxlength="4"></TD></TR>

<TR><td>身体消費</td><TD><input type="text" size="4" value="$syo_sintai_syouhi" name="syo_sintai_syouhi" maxlength="4"></TD></TR>
<TR><td>頭脳消費</td><TD><input type="text" size="4" value="$syo_zunou_syouhi" name="syo_zunou_syouhi" maxlength="4"></TD></TR>
<TR><td>耐久</td><TD><input type="text" size="2" value="$syo_taikyuu" name="syo_taikyuu" maxlength="2">$taitai</TD></TR>

<TR><td>間隔（分）</td><TD><input type="text" size="3" value="$syo_kankaku" name="syo_kankaku" maxlength="3"></TD></TR>
<TR><td>値段<BR>問屋での価格です</td><TD><input type="text" size="10" value="$syo_nedan" name="syo_nedan" maxlength="10"></TD></TR>

<TR><td>在庫（$zaiko_tyousetutiが下限）</td><TD><input type="text" size="2" value="$syo_zaiko" name="syo_zaiko" maxlength="2">×$zaiko_tyousetuti
<BR>この数字／$zaiko_tyousetutiが食堂やデパートに並び
<BR>この数字の$ton_zaiko_tyousei倍が問屋に並びます</TD></TR>

<TR><TR><td colspan="2">
効果について<BR><BR>
特別コメント　※専門店限定商品。※秘伝商品。※移動手段です。商品目=ランダム品<br>
$kouka_set
</TR>
<TR><td>効果</td><TD>$kou1　　<input type="text" size="2" value="$sonoiryoku" name="sonoiryoku" maxlength="2">　　所属<select name="zokusei_in">
$zokusei_disp<!-- koko2006/10/16 -->
</select></TD></TR>
<TR><td>コメント</td>
<TD>
<input type="text" size="30" value="$syo_comment" name="syo_comment"  maxlength="30"><BR></TD></TR>
<TR><td colspan="2" align="center">
	<input type="submit" value="修正／投稿">
		</form>
</TR>
</table>
EOM

	print "<div align=\"right\">オリジナル:ゆかにゃん<br>Edit:たっちゃん<div>\n";
	print "</body></html>\n";
	exit;


}	

#書き込み処理
sub item_make_w1{
	$item_file="$toukou_file";
	open(OL,"< $item_file") || &error("Open Error : $toukou_file");
	eval{ flock (OL, 1); };
	@item_all = <OL>;
	close(OL); #koko2007/12/08 Bag
	if($in{'dou'} eq "naosi"){
		$in{'item_no'}=$in{'ss'};
	}else{
		$s_kaku=@item_all;
		$in{'item_no'}=$s_kaku;
	}
	
	&header(syokudou_style);
	
	if($in{'syo_hinmoku'}eq""){
		&error("商品名が空欄です");
	}elsif ($in{'syo_hinmoku'} =~('[&!*()/ ,<>]')){ #koko2007/10/21 =を許可
		&error("使用禁止文字が含まれています<BR>[&!*()/.,<>]半角スペース\\");
	}
	if ($in{'syo_comment'} =~('[&!*()/ =,<>]')){
		&error("使用禁止文字が含まれています<BR>[&!*()/=.,<>]半角スペース\\");
	}

	@hankaku = ("$in{'syo_kokugo'}","$in{'syo_suugaku'}","$in{'syo_rika'}","$in{'syo_syakai'}","$in{'syo_eigo'}","$in{'syo_ongaku'}","$in{'syo_bijutu'}","$in{'syo_etti'}","$in{'syo_looks'}","$in{'syo_tairyoku'}","$in{'syo_kenkou'}","$in{'syo_speed'}","$in{'syo_power'}","$in{'syo_wanryoku'}","$in{'syo_kyakuryoku'}","$in{'syo_nedan'}","$in{'syo_love'}","$in{'syo_unique'}","$in{'syo_taikyuu'}","$in{'syo_kankaku'}","$in{'syo_zaiko'}","$in{'syo_cal'}","$in{'syo_siyou_date'}","$in{'syo_sintai_syouhi'}","$in{'syo_zunou_syouhi'}","$in{'sonoiryoku'}");

	$xx=0;
	foreach (@hankaku){
		if ($_ =~('[&!*()/ =,<>]')){
			&error("使用禁止文字が含まれています<BR>[&!*()/=.,<>]半角スペース\\");
		}elsif($_ =~/\\/){
			&error("使用禁止文字が含まれています<BR>[&!*()/=.,<>]半角スペース\\");
		}
		if($_<0){$_ = $_ * -1;}
		
		if($_ =~ /[^0-9]/){&error("数値入力欄に数値以外が記入されてます");}
	}
		if($in{'kou1'} eq"無" || $in{'kou1'} eq "クレジット"){
			$in{'syo_kouka'} ="$in{'kou1'}";
		}else{
			$in{'syo_kouka'} = "$in{'kou1'},$in{'sonoiryoku'}";
		}
#koko2006/10/12
		if ($in{'syo_kouka'} eq "無"){
			$in{'syo_kouka'} = $in{'zokusei_in'};
		}else{
			if ($in{'zokusei_in'} ne "無" && $in{'kou1'} ne "クレジット"){
		#	if ($in{'zokusei_in'} ne "無"){ #To be, or not to be.
				$in{'syo_kouka'} .= ",$in{'zokusei_in'}";
			}
		}
#kokoend


	if($in{'dou'} eq "naosi"){
		
		$item_all[($in{'item_no'})]="$in{'ty'}<>$in{'syo_hinmoku'}<>$in{'syo_kokugo'}<>$in{'syo_suugaku'}<>$in{'syo_rika'}<>$in{'syo_syakai'}<>$in{'syo_eigo'}<>$in{'syo_ongaku'}<>$in{'syo_bijutu'}<>$in{'syo_kouka'}<>$in{'syo_looks'}<>$in{'syo_tairyoku'}<>$in{'syo_kenkou'}<>$in{'syo_speed'}<>$in{'syo_power'}<>$in{'syo_wanryoku'}<>$in{'syo_kyakuryoku'}<>$in{'syo_nedan'}<>$in{'syo_love'}<>$in{'syo_unique'}<>$in{'syo_etti'}<>$in{'syo_taikyuu'}<>$in{'tai'}<>$in{'syo_kankaku'}<>$in{'syo_zaiko'}<>$in{'syo_cal'}<>$in{'syo_siyou_date'}<>$in{'syo_sintai_syouhi'}<>$in{'syo_zunou_syouhi'}<>$in{'syo_comment'}<>$name<>$in{'tanka'}<>$in{'tokubai'}<>\n";
	}else{
		$in{'item_no'}=@item_all+1;
		$item_t="$in{'ty'}<>$in{'syo_hinmoku'}<>$in{'syo_kokugo'}<>$in{'syo_suugaku'}<>$in{'syo_rika'}<>$in{'syo_syakai'}<>$in{'syo_eigo'}<>$in{'syo_ongaku'}<>$in{'syo_bijutu'}<>$in{'syo_kouka'}<>$in{'syo_looks'}<>$in{'syo_tairyoku'}<>$in{'syo_kenkou'}<>$in{'syo_speed'}<>$in{'syo_power'}<>$in{'syo_wanryoku'}<>$in{'syo_kyakuryoku'}<>$in{'syo_nedan'}<>$in{'syo_love'}<>$in{'syo_unique'}<>$in{'syo_etti'}<>$in{'syo_taikyuu'}<>$in{'tai'}<>$in{'syo_kankaku'}<>$in{'syo_zaiko'}<>$in{'syo_cal'}<>$in{'syo_siyou_date'}<>$in{'syo_sintai_syouhi'}<>$in{'syo_zunou_syouhi'}<>$in{'syo_comment'}<>$name<>$in{'tanka'}<>$in{'tokubai'}<>\n";
		push (@item_all,$item_t);
		
#koko2005/12/6
		if ($#item_all >= $item_max){
			$#item_all = $item_max - 1;
			&error("アイテム投稿が上限になってます。");
		}
#kokoend
		
	}
	open(OLOUT,">$item_file") || &error("$item_fileに書き込みが出来ません");
	eval{ flock (OL, 2); };
	print OLOUT @item_all;
	close(OLOUT);
	&unlock;
	print <<"EOM";
<table border="1" cellspacing="1" cellpadding="5" align="center" class="yosumi">
<TR><TD>ＩＤ</td><td>$in{'item_no'}</td></TR>

<TR><TD>種類</td><td>$in{'ty'}</td></TR>
<TR><TD>品目</td><TD>$in{'syo_hinmoku'}</TD></TR>

<TR><td>国</td><TD>$in{'syo_kokugo'}</TD></TR>
<TR><td>数</td><TD>$in{'syo_suugaku'}</TD></TR>
<TR><td>理</td><TD>$in{'syo_rika'}</TD></TR>
<TR><td>社</td><TD>$in{'syo_syakai'}</TD></TR>
<TR><td>英</td><TD>$in{'syo_eigo'}</TD></TR>
<TR><td>音</td><TD>$in{'syo_ongaku'}</TD></TR>
<TR><td>美</td><TD>$in{'syo_bijutu'}</TD></TR>
<TR><td>ル</td><TD>$in{'syo_looks'}</TD></TR>
<TR><td>体力</td><TD>$in{'syo_tairyoku'}</TD></TR>
<TR><td>健</td><TD>$in{'syo_kenkou'}</TD></TR>
<TR><td>ス</td><TD>$in{'syo_speed'}</TD></TR>
<TR><td>パ</td><TD>$in{'syo_power'}</TD></TR>
<TR><td>腕</td><TD>$in{'syo_wanryoku'}</TD></TR>
<TR><td>脚</td><TD>$in{'syo_kyakuryoku'}</TD></TR>
<TR><td>L</td><TD>$in{'syo_love'}</TD></TR>
<TR><td>面</td><TD>$in{'syo_unique'}</TD></TR>
<TR><td>H</td><TD>$in{'syo_etti'}</TD></TR>
<TR><td>カロリー</td><TD>$in{'syo_cal'}</TD></TR>
<TR><td>身体消費</td><TD>$in{'syo_sintai_syouhi'}</TD></TR>
<TR><td>頭脳消費</td><TD>$in{'syo_zunou_syouhi'}</TD></TR>
<TR><td>耐久</td><TD>$in{'syo_taikyuu'}$in{'tai'}</TD></TR>

<TR><td>間隔（分）</td><TD>$in{'syo_kankaku'}</TD></TR>
<TR><td>値段</td><TD>$in{'syo_nedan'}</TD></TR>
<TR><td>在庫</td><TD>$in{'syo_zaiko'}</TD></TR>
<!--<TR><td>効果</td><TD>$in{'kou1'}$in{'sonoiryoku'}</TD></TR>-->
<TR><td>効果</td><TD>$in{'syo_kouka'}</TD></TR>
<TR><td>コメント</td><TD>$in{'syo_comment'}</TD></TR>
	<TR><td colspan="2" align="center">
	<form method="POST" action="$this_script">
	<input type="hidden" name="mode" value="item_make">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="k_id" value="$in{'k_id'}"> <!-- 抜けていました2007/11/18 -->
	<input type="hidden" name="item_ty" value="$in{'item_ty'}">
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="hidden" name="t_ty" value="new">
	<input type="submit" value="戻る"></TR>
</table></form>
EOM

	print "<div align=\"right\">オリジナル:ゆかにゃん<br>Edit:たっちゃん<div>\n";
	print "</body></html>\n";
	exit;

}
# アイテム処理
sub make{
	@item_all = ();
	if($in{'t_ty'} eq "new" || $in{'syo_hinmoku'} eq ""){
		$item_file="$toukou_file";
		open(OL,"< $item_file") || &error("Open Error : $toukou_file");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya0"){
		$item_file=$tonya0;
		open(OL,"< $item_file") || &error("Open Error : $tonya1");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya1"){
		$item_file=$tonya1;
		open(OL,"< $item_file") || &error("Open Error : $tonya1");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya2"){
		$item_file=$tonya2;
		open(OL,"< $item_file") || &error("Open Error : $tonya2");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya3"){
		$item_file=$tonya3;
		open(OL,"< $item_file") || &error("Open Error : $tonya3");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya4"){
		$item_file=$tonya4;
		open(OL,"< $item_file") || &error("Open Error : $tonya4");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'tonya'} eq "tonya5"){
		$item_file=$tonya5;
		open(OL,"< $item_file") || &error("Open Error : $tonya5");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}elsif($in{'t_ty'} eq "moto"){
		$item_file= $toukou_file; #koko2006/12/10
		open(OL,"< $item_file") || &error("Open Error : $toukou_file");
		eval{ flock (OL, 1); };
		@item_all = <OL>;
		close(OL);
	}else{&error("元ファイルがありません。");}

	&syouhin_sprit($item_all[$in{'syo_hinmoku'}]);
	$moto_syo_syubetu = $syo_syubetu;
	$moto_syo_hinmoku = $syo_hinmoku;

	@item_all_out = ();
	@new_sybetu = ();
	@new_item_out = ();
	@new_item_out0 = ();

	unless( -e $in{'fail'}){&error("ファイルが存在しません。");}
	open(OL,"< $in{'fail'}") || &error("Open Error : $in{'fail'}");
	eval{ flock (OL, 1); };
	@item_all_out = <OL>;
	close(OL); #koko2007/12/08 Bag

	foreach (@item_all_out){
		&syouhin_sprit($_);
		if($moto_syo_syubetu eq $syo_syubetu){
			if($in{'delet'} && $moto_syo_hinmoku eq $syo_hinmoku){next;}
			if($moto_syo_hinmoku eq $syo_hinmoku){&error("二重登録になります。");}
			push @new_sybetu,$_;
			next;
		}
		push @new_item_out,$_;
	}
	if($in{'fa'}){push @new_sybetu,$item_all[$in{'syo_hinmoku'}]};
	@new_item_out0 = (@new_item_out,@new_sybetu);
	@item_all = ();

	open(OL,"> $in{'fail'}") || &error("Open Error : $in{'fail'}");
	eval{ flock (OL, 2); };
	print OL @new_item_out0;
	close(OL);

#	&error("test $in{'syo_hinmoku'}");
	&item_make;
}
