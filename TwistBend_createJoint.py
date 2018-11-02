import maya.cmds as mc

def TtoB():
	#create joint
	jnt = mc.ls(sl=True)
	tar = mc.listRelatives('{}'.format(jnt[0]))
	par = mc.listRelatives('{}'.format(jnt[0]), p=True)
	twi_trs = mc.getAttr('{}.translateX'.format(jnt[0]))
	jnt_trs = mc.getAttr('{}.worldMatrix[0]'.format(jnt[0]))
	par_trs = mc.getAttr('{}.worldMatrix[0]'.format(par[0]))
	jnt_orix = mc.getAttr('{}.jointOrientX'.format(jnt[0]))
	jnt_oriy = mc.getAttr('{}.jointOrientY'.format(jnt[0]))
	jnt_oriz = mc.getAttr('{}.jointOrientZ'.format(jnt[0]))
	twi_trs = twi_trs / 2
	jnt_rot = [-1 * jnt_orix, -1 * jnt_oriy, -1 * jnt_oriz] 

	twi = mc.joint(n='{}_twist'.format(jnt[0]), rad=0.3, p=(par_trs[12],par_trs[13],par_trs[14]))
	ben = mc.joint(n='{}_bend'.format(jnt[0]), rad=0.3, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
	mc.parent('{}'.format(twi), '{}'.format(par[0]))
	mc.joint('{}'.format(twi), e=True, oj='xyz', sao='yup')
	mc.setAttr('{}.translateX'.format(twi), twi_trs)
	mc.setAttr('{}.translateX'.format(ben), twi_trs)
	mc.setAttr('{}.jointOrientX'.format(twi), 0)
	mc.setAttr('{}.jointOrientY'.format(twi), 0)
	mc.setAttr('{}.jointOrientZ'.format(twi), 0)
	mc.setAttr('{}.jointOrientX'.format(ben), jnt_orix)
	mc.setAttr('{}.jointOrientY'.format(ben), jnt_oriy)
	mc.setAttr('{}.jointOrientZ'.format(ben), jnt_oriz)

win = mc.window(t='TtoBtest', widthHeight=(200,30))
mc.columnLayout()
mc.button(l='TtoB', c='TtoB()')
mc.showWindow(win)