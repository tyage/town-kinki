#!/usr/bin/perl

#--------------------------------------#
#            �@ �}�b�v            �@�@ #
#                                  �@�@#
#�@�@Copyright (c) 2008�@�`���Q   �@�@ #
# �@ web�Fhttp://tyage.a.orn.jp/ �@�@  #
# �@ mail�Ftyage2@nifmail.jp     �@�@  #
#--------------------------------------#

require './town_ini.cgi';
require './town_lib.pl';
&decode;

if($in{'mode'} eq "idou"){&idou;}
if($in{'mode'} eq "map"){&map;}

exit;

######################
#�@�ȉ��T�u���[�`���@#
######################
sub map{
	#=====�Q�X�g�t�@�C��OPEN=====#
	open(GST,"< $guestfile");
	eval{ flock (GST, 1); };
	foreach(<GST>){
		($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
		if($hyouzi_check eq "off"){next;}
		if($mati_name eq ""){$humei .= "$sanka_name<br>";}
		elsif($mati_name==0){$keihan .= "$sanka_name<br>";}
		elsif($mati_name==1){$biwako .= "$sanka_name<br>";}
		elsif($mati_name==2){$nara .= "$sanka_name<br>";}
		elsif($mati_name==3){$wakayama .= "$sanka_name<br>";}
		else{$humei .= "$sanka_name<br>";}
	}
	close(GST);

	if(!$keihan){$keihan="�N�����܂���";}
	if(!$biwako){$biwako="�N�����܂���";}
	if(!$nara){$nara="�N�����܂���";}
	if(!$wakayama){$wakayama="�N�����܂���";}
	if(!$humei){$humei="�N�����܂���";}

	#=====MAP�\��=====#
	&header(ginkou_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi height="100"><tr>
<td bgcolor=#ffffff>���z�C�ȉw��<br>
�u�����͌��Ă̂Ƃ���w����B<br>
�@�ł����ʂ̉w���Ⴀ�Ȃ��񂾁I<br>
�@���������B��Ă�l�ȊO���ǂ��ɂ��邩�u���ŕ��������Ⴄ�A����\�\\�ȉw�Ȃ񂾂�B<br>
�@���̂l�`�o����d�Ԃ��g���΂ǂ��ł��������B�v</td>
<td  bgcolor=#333333 align=center width=35%>
<font color="#ffffff" size="5"><b>�r�s�`�s�h�n�m</b></font>
</td>
</tr></table>
<br>
<center>
<table width="400" cellpadding="0" cellspacing="0" border="1" style="z-index:1;"><tr>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokuteki value="0">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/keihansin-s.gif" width="200" height="150" title="����_�X�g���[�g" align="left" valign="top"><center><input type=submit value=����_�X�g���[�g�� style="border:1px solid;"></center><br><font color="#ffffff"><b>$keihan</b></font></td>
</form>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokuteki value="1">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/biwako-s.gif" width="200" height="150" title="�ߍ]���C�N" align="left" valign="top"><center><input type=submit value=�ߍ]���C�N�� style="border:1px solid;"></center><br><font color="#ffffff"><b>$biwako</b></font></td>
</form>
</tr><tr>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokuteki value="3">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/wakayama-s.gif" width="200" height="150" title="�a�̎R�A�C�����h" align="left" valign="top"><center><input type=submit value=�a�̎R�A�C�����h style="border:1px solid;"></center><br><font color="#ffffff"><b>$wakayama</b></font></td>
</form>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokuteki value="2">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/nara-s.gif" width="200" height="150" title="�ޗǃV�e�B" align="left" valign="top"><center><input type=submit value=�ޗǃV�e�B style="border:1px solid;"></center><br><font color="#ffffff"><b>$nara</b></font></td>
</form>
</tr></table><br>
�ʒu���s���Ȑl<br>
<font color="#ffffff"><b>$humei</b></font>
</center>
EOM
	&hooter("login_view","�X�ɖ߂�");
exit;
}

sub idou{
	if($in{'maemati'} eq ""){&error("���Ȃ��͂ǂ����痈���́H");}
	if($in{'mokuteki'} eq ""){&error("���Ȃ��͂ǂ��ɍs���́H");}
	if($in{'maemati'}==$in{'mokuteki'}){&error("�X�ɖ߂��Ȃ畁�ʂ̖߂�΂����ł��傤��");}
	$matiidou_time2=5;

	if($in{'maemati'} == 0 and $in{'mokuteki'} == 1 or $in{'maemati'} == 1 and $in{'mokuteki'} == 0){$nedan=950;}
	elsif($in{'maemati'} == 0 and $in{'mokuteki'} == 2 or $in{'maemati'} == 2 and $in{'mokuteki'} == 0){$nedan=780;}
	elsif($in{'maemati'} == 0 and $in{'mokuteki'} == 3 or $in{'maemati'} == 3 and $in{'mokuteki'} == 0){$nedan=1210;}
	elsif($in{'maemati'} == 1 and $in{'mokuteki'} == 2 or $in{'maemati'} == 2 and $in{'mokuteki'} == 1){$nedan=950;}
	elsif($in{'maemati'} == 1 and $in{'mokuteki'} == 3 or $in{'maemati'} == 3 and $in{'mokuteki'} == 1){$nedan=2210;}
	elsif($in{'maemati'} == 2 and $in{'mokuteki'} == 3 or $in{'maemati'} == 3 and $in{'mokuteki'} == 2){$nedan=1530;}
	else{&error("�C���I�ɃG���[");}

	$money -= $nedan;

	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	#=====�Q�X�g�t�@�C��OPEN=====#
	open(GST,"< $guestfile");
	eval{ flock (GST, 1); };
	foreach(<GST>){
		 ($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
		 if($hyouzi_check eq "off"){next;}
		 if($mati_name==0 or !$mati_name){$keihan .= "$sanka_name<br>";}
		 elsif($mati_name==1){$biwako .= "$sanka_name<br>";}
		 elsif($mati_name==2){$nara .= "$sanka_name<br>";}
		 elsif($mati_name==3){$wakayama .= "$sanka_name<br>";}
		 else{&error("�G���[");}
	}
	close(GST);
	if(!$keihan){$keihan="�N�����܂���";}
	if(!$biwako){$biwako="�N�����܂���";}
	if(!$nara){$nara="�N�����܂���";}
	if(!$wakayama){$wakayama="�N�����܂���";}

	#=====�ړ����\��=====#
	&header(syokudou_style);
	print <<"EOM";
<script language="JavaScript"><!--
var TimeID;
var counts=$matiidou_time2;
window.setTimeout("run()",1000);
function run(){
counts--;
document.getElementById("time").innerHTML = counts;
if(counts>0){timeID = setTimeout("run()",1000);}
}
$disp_in
//--></script>

<br><br><br><br><table  border=0  cellspacing="5" cellpadding="0" width=200 align=center bgcolor=#ffffcc><tr><td><div align=center style=\"font-size:11px\">�d�Ԃňړ���...<br><span id=\"time\">$matiidou_time2</span>�b�قǂ��҂����������B<br>$nedan�~�x�����܂����B</div></td></tr></table>

<center>
<table width="400" cellpadding="0" cellspacing="0" border="1" style="z-index:1;"><tr>
<td background="img/keihansin-s.gif" width="200" height="150" title="����_�X�g���[�g" align="left" valign="top"><center><font color="red"><b>����_�X�g���[�g</b></font></center><br><font color="#ffffff"><b>$keihan</b></font></td>
<td background="img/biwako-s.gif" width="200" height="150" title="�ߍ]���C�N" align="left" valign="top"><center><font color="red"><b>�ߍ]���C�N</b></font></center><br><font color="#ffffff"><b>$biwako</b></font></td>
</tr><tr>
<td background="img/wakayama-s.gif" width="200" height="150" title="�a�̎R�A�C�����h" align="left" valign="top"><center><font color="red"><b>�a�̎R�A�C�����h</b></font></center><br><font color="#ffffff"><b>$wakayama</b></font></td>
<td background="img/nara-s.gif" width="200" height="150" title="�ޗǃV�e�B" align="left" valign="top"><center><font color="red"><b>�ޗǃV�e�B</b></font></center><br><font color="#ffffff"><b>$nara</b></font></td>
</tr></table>
</center>

<form method=POST name=f_idou action="$script">
<input type=hidden name=mode value="login_view">
<input type=hidden name=town_no value="$in{'mokuteki'}">
<input type=hidden name=idou value="$idou_time">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=ziko_flag value="off">
<input type=hidden name=maigo value="">
</form>
EOM

exit;
}