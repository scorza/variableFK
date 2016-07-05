import functools
import maya.cmds as mc
import pymel.core as pmc

from PySide import QtCore as qc
from PySide import QtGui as qg
from shiboken import wrapInstance

import maya.OpenMayaUI as omui

def maya_main_window():
    '''
    Return the Maya main window as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), qg.QWidget)
    

class VFK_UI(qg.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(VFK_UI, self).__init__(parent)
    
    def format_widget(self, lbl_text = 'Label text', sub_text = 'Default value'):
        lbl = qg.QLabel(lbl_text)
        le = qg.QLineEdit()
        le.setMinimumSize(75,20)
        le.setMaximumSize(75,20)
        sub = qg.QLabel(sub_text)
        sub.setStyleSheet('color: rgb(140,140,140)')
        
        layoutA = qg.QVBoxLayout()
        layoutA.setContentsMargins(0,0,0,0)        
        layoutA.setSpacing(0)
        layoutB = qg.QHBoxLayout()
        layoutB.setContentsMargins(0,0,0,0)
        layoutB.setSpacing(0)     
        layoutB.addWidget(lbl)
        layoutB.addWidget(le)
        layoutA.addLayout(layoutB)
        layoutA.addWidget(sub)

        widget = qg.QWidget()
        widget.setLayout(layoutA)

        return_tuple = (widget, le)
        
        return return_tuple
    
    def create_ui(self):
        pmc.undoInfo(openChunk=True)

        self.setWindowTitle('VFK Rig Creator')
        self.setWindowFlags(qc.Qt.Tool)
        self.setMinimumSize(300, 400)
        self.setMaximumWidth(300)
        
        self.create_controls()
        self.create_layout()
        self.create_connections()

        pmc.undoInfo(closeChunk=True)
        
    def create_controls(self):
        self.header_lbl = qg.QLabel('Select start joint, then end joint')
        self.credit_lbl = qg.QLabel('Automates creation of VFK rig after Jeff Brodsky')
        self.credit_lbl.setStyleSheet('color: rgb(140,140,140)')
        self.link_lbl = qg.QLabel('https://vimeo.com/49353110')
        self.link_lbl.setStyleSheet('color: rgb(140,140,140)')
        
        self.name_widget, self.name_le = self.format_widget(lbl_text = 'Name prefix', 
                                                                sub_text = 'Default = nameOfTopJoint_ \nNames should be unique.')        
        
        self.joints_widget, self.joints_le = self.format_widget(lbl_text = 'Total number of joints', 
                                                                sub_text = 'Default = 20')
        self.controls_widget, self.controls_le = self.format_widget(lbl_text = 'Number of controls', 
                                                                    sub_text = 'Default = 3')
        self.control_radius_widget, self.control_radius_le = self.format_widget(lbl_text = 'Control radius', 
                                                                                sub_text = 'Default = 4.0')
        self.joint_radius_widget, self.joint_radius_le= self.format_widget(lbl_text = 'Joint radius', 
                                                                            sub_text = 'Default = 0.25')
        self.joint_prefix_widget, self.joint_prefix_le = self.format_widget(lbl_text = 'Joint prefix', 
                                                                            sub_text = 'Default = "joint_"')
        self.joint_grp_prefix_widget, self.joint_grp_prefix_le = self.format_widget(lbl_text = 'Joint group prefix', 
                                                                                    sub_text = 'Default = "vfk_grp_"')        
        self.control_prefix_widget, self.control_prefix_le = self.format_widget(lbl_text = 'Control prefix', 
                                                                                sub_text = 'Default = "CTRL_vfk_"')
        self.control_grp_prefix_widget, self.control_grp_prefix_le = self.format_widget(lbl_text = 'Control group prefix', 
                                                                                          sub_text = 'Default = "OFF_CTRL_vfk_"')
        # Bone translate axis widget
        self.bone_trans_axis_widget = qg.QWidget()
        bone_trans_axis_lbl = qg.QLabel('Set bone main axis')
        self.bone_trans_axis_radX = qg.QRadioButton('x')
        self.bone_trans_axis_radY = qg.QRadioButton('y')
        self.bone_trans_axis_radZ = qg.QRadioButton('z')
        self.bone_trans_axis_radX.setChecked(True)
        bone_trans_axis_lbl.setMaximumHeight(20)
        self.bone_trans_axis_radX.setMaximumHeight(20)
        self.bone_trans_axis_radY.setMaximumHeight(20)
        self.bone_trans_axis_radZ.setMaximumHeight(20)
        
        bone_trans_axis_sub = qg.QLabel('Default = x')
        bone_trans_axis_sub.setStyleSheet('color: rgb(140,140,140)')
        
        bone_trans_axis_layoutA = qg.QVBoxLayout()
        bone_trans_axis_layoutA.setContentsMargins(0,0,0,0)
        bone_trans_axis_layoutA.setSpacing(0)

        bone_trans_axis_layoutB = qg.QHBoxLayout()
        bone_trans_axis_layoutB.setContentsMargins(0,0,0,0)
        bone_trans_axis_layoutB.setSpacing(0)
        
        bone_trans_axis_layoutC = qg.QHBoxLayout()
        bone_trans_axis_layoutC.setContentsMargins(0,0,0,0)               
        bone_trans_axis_layoutC.setSpacing(10)
        bone_trans_axis_layoutC.setAlignment(qc.Qt.AlignRight)
        

        bone_trans_axis_layoutB.addWidget(bone_trans_axis_lbl)
        bone_trans_axis_layoutB.addLayout(bone_trans_axis_layoutC)
        
        
        bone_trans_axis_layoutC.addWidget(self.bone_trans_axis_radX)
        bone_trans_axis_layoutC.addWidget(self.bone_trans_axis_radY)
        bone_trans_axis_layoutC.addWidget(self.bone_trans_axis_radZ)

        bone_trans_axis_layoutA.addLayout(bone_trans_axis_layoutB)
        bone_trans_axis_layoutA.addWidget(bone_trans_axis_sub)
        bone_trans_axis_sub.setAlignment(qc.Qt.AlignTop)

        self.bone_trans_axis_widget.setLayout(bone_trans_axis_layoutA)
        
        # Bone up axis widget
        self.bone_up_axis_widget = qg.QWidget()
        bone_up_axis_lbl = qg.QLabel('Set bone up axis')
        self.bone_up_axis_radX = qg.QRadioButton('x')
        self.bone_up_axis_radY = qg.QRadioButton('y')
        self.bone_up_axis_radZ = qg.QRadioButton('z')
        self.bone_up_axis_radZ.setChecked(True)
        bone_up_axis_lbl.setMaximumHeight(20)
        self.bone_up_axis_radX.setMaximumHeight(20)
        self.bone_up_axis_radY.setMaximumHeight(20)
        self.bone_up_axis_radZ.setMaximumHeight(20)
        
        bone_up_axis_sub = qg.QLabel('Default = z')
        bone_up_axis_sub.setStyleSheet('color: rgb(140,140,140)')
        
        bone_up_axis_layoutA = qg.QVBoxLayout()
        bone_up_axis_layoutA.setContentsMargins(0,0,0,0)
        bone_up_axis_layoutA.setSpacing(0)

        bone_up_axis_layoutB = qg.QHBoxLayout()
        bone_up_axis_layoutB.setContentsMargins(0,0,0,0)
        bone_up_axis_layoutB.setSpacing(0)
        
        bone_up_axis_layoutC = qg.QHBoxLayout()
        bone_up_axis_layoutC.setContentsMargins(0,0,0,0)               
        bone_up_axis_layoutC.setSpacing(10)
        bone_up_axis_layoutC.setAlignment(qc.Qt.AlignRight)
        

        bone_up_axis_layoutB.addWidget(bone_up_axis_lbl)
        bone_up_axis_layoutB.addLayout(bone_up_axis_layoutC)
        
        
        bone_up_axis_layoutC.addWidget(self.bone_up_axis_radX)
        bone_up_axis_layoutC.addWidget(self.bone_up_axis_radY)
        bone_up_axis_layoutC.addWidget(self.bone_up_axis_radZ)

        bone_up_axis_layoutA.addLayout(bone_up_axis_layoutB)
        bone_up_axis_layoutA.addWidget(bone_up_axis_sub)
        bone_up_axis_sub.setAlignment(qc.Qt.AlignTop)

        self.bone_up_axis_widget.setLayout(bone_up_axis_layoutA)        

        # Create VFK button
        self.create_vfk_btn = qg.QPushButton('Create VFK Rig')
        self.create_vfk_btn.setMaximumSize(200,100)
        #btn_grad = qg.QLinearGradient(x1:0, y1:0, x2:1, y2:0, stop: 0 red, stop: 1 blue)
        #image_path = pmc.internalVar(upd=True) + 'icons/jiii_buttonBG.png'
        #self.create_vfk_btn.setStyleSheet('background-image: url(' + image_path + ');'
        #                                  'border: solid black 1px;')
        self.create_vfk_btn.setStyleSheet('border: solid black 1px;'
                                          'background-color: QLinearGradient(x1:0, y1:0, x2:1, y2:0, stop: 0 rgb(255,0,255), stop: 1 rgb(0,255,255)')
        
        self.close_on_create_chk = qg.QCheckBox('Close window on rig creation')
        self.close_on_create_chk.setCheckState(qc.Qt.Checked)
        
    def create_layout(self):
        tab_widget = qg.QTabWidget()
        basic_tab_page = qg.QWidget()
        advanced_tab_page = qg.QWidget()
        basic_layout = qg.QVBoxLayout(basic_tab_page)
        advanced_layout = qg.QVBoxLayout(advanced_tab_page)
        btn_layout = qg.QHBoxLayout()

        basic_layout.addWidget(self.name_widget)
        basic_layout.addWidget(self.joints_widget)
        basic_layout.addWidget(self.controls_widget)
        basic_layout.setAlignment(qc.Qt.AlignTop)
        
        advanced_layout.addWidget(self.control_radius_widget)
        advanced_layout.addWidget(self.joint_radius_widget)
        advanced_layout.addWidget(self.joint_prefix_widget)
        advanced_layout.addWidget(self.joint_grp_prefix_widget)
        advanced_layout.addWidget(self.control_prefix_widget)
        advanced_layout.addWidget(self.control_grp_prefix_widget)
        advanced_layout.addWidget(self.bone_trans_axis_widget)
        advanced_layout.addWidget(self.bone_up_axis_widget)
        advanced_layout.setAlignment(qc.Qt.AlignTop)

        tab_widget.addTab(basic_tab_page, 'Basic')
        tab_widget.addTab(advanced_tab_page, 'Advanced')
        
        btn_layout.addWidget(self.create_vfk_btn)
        #btn_layout.addWidget(self.close_on_create_chk)
                
        main_layout = qg.QVBoxLayout()
        main_layout.setContentsMargins(10,10,10,10)

        main_layout.addWidget(self.header_lbl)
        main_layout.addWidget(self.credit_lbl)
        main_layout.addWidget(self.link_lbl)
        main_layout.addWidget(tab_widget)
        main_layout.addLayout(btn_layout)
                        
        main_layout.setAlignment(qc.Qt.AlignTop)
        self.setLayout(main_layout)
    
    def create_connections(self):
        self.create_vfk_btn.clicked.connect(self.create_vfk)

        #self.create_vfk_btn.clicked.connect(self._testBind)
        

    ###############
    # MAIN FUNCTION
    ###############
    def create_vfk(self, name = "", numJoints=20.0, numControls=3.0, controlRadius = 4.0, 
                  jointRadius=0.25, jointPrefix = 'joint_', jointGroupPrefix ='vfk_grp_',
                  controlPrefix = 'CTRL_vfk_', controlGroupPrefix = 'OFF_CTRL_vfk_', 
                  boneTranslateAxis = '.tx', boneUpAxis = [0,0,1]):
        
        '''
        if self.close_on_create_chk.checkState() == qc.Qt.Checked:
            self.close
        '''
        
        
        pmc.undoInfo(openChunk=True)
        
        ### Get top and end joints, check for parents/children
        sels = pmc.ls(sl=1)
        topJoint = sels[0]
        endJoint = sels[1]
        
        try:
            print topJoint, ' and ', endJoint, ' selected.'
            ### pmc.listRelatives(topJoint, children=True, type='joint')
        except IndexError:
            print 'Error: Select a joint and an immediate child joint.'
        
            
    
        endChild = pmc.listRelatives(endJoint, c=True)
        if endChild:
            linkJointEnd = pmc.duplicate(endJoint, parentOnly=True, n=endJoint + '_LINK')
            pmc.setAttr(linkJointEnd[0] + '.radius', jointRadius * 2)
            pmc.parent(endChild, linkJointEnd)
            pmc.parent(linkJointEnd, w=True)
            
        topParent = pmc.listRelatives(topJoint, p=True)
        if topParent:
            linkJointTop = pmc.duplicate(topJoint, parentOnly=True,  n=topJoint + '_LINK')
            pmc.setAttr(linkJointTop[0] + '.radius', jointRadius * 2)
            pmc.parent(linkJointTop, topParent)
            pmc.parent(topJoint, linkJointTop)
                
        ### Check basic user-defined values
        if self.name_le.text() != "":
            name = self.name_le.text()
        else:
            name = str(topJoint) + '_'
        if self.joints_le.text() != "":
            numJoints = float(self.joints_le.text())
        if self.controls_le.text() != "":
            numControls = float(self.controls_le.text())
 
        ### Check advanced user-defined values
        if self.control_radius_le.text() != "":
            controlRadius = float(self.control_radius_le.text())
        if self.joint_radius_le.text() != "":
            jointRadius = float(self.joint_radius_le.text())
        if self.joint_prefix_le.text() != "":
            jointPrefix = self.joint_prefix_le.text()
        if self.joint_grp_prefix_le.text() != "":
            jointGroupPrefix = self.joint_grp_prefix_le.text()
        if self.control_prefix_le.text() != "":
            controlPrefix = self.control_prefix_le.text()
        if self.control_grp_prefix_le.text() != "":
            controlGroupPrefix = self.control_grp_prefix_le.text()
        
        if self.bone_trans_axis_radX.isChecked() == True and self.bone_up_axis_radX.isChecked() == True:
            print 'Warning: bone main axis and bone up axis cannot be same.'
            return
        if self.bone_trans_axis_radY.isChecked() == True and self.bone_up_axis_radY.isChecked() == True:
            print 'Warning: bone main axis and bone up axis cannot be same.'
            return
        if self.bone_trans_axis_radZ.isChecked() == True and self.bone_up_axis_radZ.isChecked() == True:
            print 'Warning: bone main axis and bone up axis cannot be same.'
            return                        
        
        if self.bone_trans_axis_radX.isChecked() == True:
            boneTranslateAxis = '.tx'
        if self.bone_trans_axis_radY.isChecked() == True:
            boneTranslateAxis = '.ty'
        if self.bone_trans_axis_radZ.isChecked() == True:
            boneTranslateAxis = '.tz'
        if self.bone_up_axis_radX.isChecked() == True:
            boneUpAxis = [1,0,0]            
        if self.bone_up_axis_radY.isChecked() == True:
            boneUpAxis = [0,1,0]
        if self.bone_up_axis_radZ.isChecked() == True:
            boneUpAxis = [0,0,1]
            
        #### ACTUAL FUNCTION PART
        nurbsWidth = pmc.getAttr(endJoint + boneTranslateAxis)

        self._jointRes(topJoint, endJoint, boneTranslateAxis= boneTranslateAxis, add= numJoints-2)

        surface = pmc.nurbsPlane(pivot=[0,0,0], axis= boneUpAxis, width=nurbsWidth, lengthRatio=0.1, 
                                 u=(numJoints-1), ch=0, n= name + 'vfk_surface')
        
        ## Uncomment to use as polyPlane instead of nurbsSurface
        ## surface = pmc.polyPlane(w=20, h=1, sx=20, sy=1, ax=[0,1,0], cuv=2, ch=0, n= name + 'vfk_surface')
        
        if boneTranslateAxis == '.ty':
            if boneUpAxis == [1,0,0]:
                pmc.setAttr(surface[0] + '.rx', -90)
            if boneUpAxis == [0,0,1]:
                pmc.setAttr(surface[0] + '.rz', -90)
            pmc.makeIdentity(surface[0], apply=True, t=0, r=1, s=0)
        
        if boneTranslateAxis == '.tz':
            if boneUpAxis == [0,1,0]:
                pmc.setAttr(surface[0] + '.ry', -90)
            pmc.makeIdentity(surface[0], apply=True, t=0, r=1, s=0)            

        surface_off = pmc.group(surface, n= name + 'OFF_surface')

        pmc.parent(surface_off, topJoint)
        if boneTranslateAxis == '.tx':
            pmc.xform(surface_off, translation = [nurbsWidth/2, 0, 0], rotation=[0,0,0])
        if boneTranslateAxis == '.ty':
            pmc.xform(surface_off, translation = [0, nurbsWidth/2, 0], rotation=[0,0,0])        
        if boneTranslateAxis == '.tz':
            pmc.xform(surface_off, translation = [0, 0, nurbsWidth/2], rotation=[0,0,0])        
        pmc.parent(surface_off, w=True)

        surface_mtx= pmc.xform(surface, q=True, ws=True, m=True)

        joints = pmc.listRelatives(topJoint, children=1, allDescendents=1)
        joints.append(topJoint)
        joints.reverse()

        for j in xrange(len(joints)):
            pmc.select(joints[j])
            pmc.rename(joints[j], jointPrefix + str(j+1))
                        
            pmc.setAttr(joints[j] + '.radius', jointRadius)
            pmc.addAttr(joints[j], ln='position', min=0, max=1, dv=0, keyable=True)
            pmc.setAttr(joints[j] + '.position', j/(numJoints-1))
            pmc.select(cl=1)

            jmtx = pmc.xform(joints[j], q=True, m=True, ws=True)
            
            if j == 0:
                off_vfk = pmc.group(em=True, n=  name + 'OFF_vfk')
                pmc.xform(off_vfk, ws=True, m=jmtx)
                root = pmc.listRelatives(joints[0], parent=True)      
                for c in xrange(int(numControls)):
                    jparent = pmc.listRelatives(joints[j], parent=True)
                    vfk_grp = pmc.group(em=True, n= name + jointGroupPrefix + 'j' + str(j+1) + '_c' + str(c+1))
                    pmc.xform(vfk_grp, ws=True, m=jmtx)
                    pmc.parent(joints[j], vfk_grp)
                    pmc.parent(vfk_grp, jparent)
                    if c == 0:
                        pmc.parent(vfk_grp, off_vfk)
                if root != None:
                    pmc.parent(off_vfk, root)
            else:
                for c in xrange(int(numControls)):
                    jparent = pmc.listRelatives(joints[j], parent=True)
                    vfk_grp = pmc.group(em=True, n= name + jointGroupPrefix + 'j' + str(j+1) + '_c' + str(c+1))
                    pmc.xform(vfk_grp, ws=True, m=jmtx)
                    pmc.parent(joints[j], vfk_grp)
                    pmc.parent(vfk_grp, jparent)

        ctrlSpacing = (nurbsWidth/(numControls+1))

        for i in xrange(int(numControls)):
            if boneTranslateAxis == '.tx':
                ctrl_normal = [1,0,0]
            if boneTranslateAxis == '.ty':
                ctrl_normal = [0,1,0]
            if boneTranslateAxis == '.tz':
                ctrl_normal = [0,0,1]
            ctrl = pmc.circle(normal=ctrl_normal, sw=360, r=controlRadius, ch=0, n= name + controlPrefix + str(i+1))
            ctrl_off = pmc.group(ctrl, n= name + controlGroupPrefix + str(i+1))
            pmc.xform(ctrl_off, ws=True, m=surface_mtx)
                        
            pmc.parent(ctrl_off, surface)
            pmc.setAttr(ctrl[0] + boneTranslateAxis, ((nurbsWidth/-2) + (ctrlSpacing*(i+1))))
            pmc.parent(ctrl_off, w=True)
            
            flcl = self._parentSurfaceFLCL(ctrl, surface[0])
            
            ctrl_mtx = pmc.xform(ctrl, q=True, m=True, ws=True)
            pmc.xform(ctrl_off, ws=True, m=ctrl_mtx)
            pmc.parent(ctrl_off, flcl[0])
            pmc.parent(ctrl, ctrl_off)
            
            min_falloff = 1/numJoints
            
            pmc.addAttr(ctrl[0], ln='position', min=0, max=10, dv=0, keyable=True)
            pmc.addAttr(ctrl[0], ln='falloff', min=min_falloff, max=1, dv=0.5, keyable=True)
            pmc.addAttr(ctrl[0], ln='numberOfJointsAffected', min=0, max=numJoints, dv=0, keyable=True)
            
            multD = pmc.createNode('multiplyDivide', n= name + 'multD_jAff_vfk_' + str(i+1))
            setR = mc.createNode('setRange', n= name + 'setR_jAff_vfk_' + str(i+1))
                
            pmc.connectAttr(ctrl[0] + '.falloff', multD + '.input1X')
            pmc.setAttr(multD + '.input2X', 2)
            pmc.setAttr(multD + '.operation', 1)
            
            pmc.connectAttr(multD + '.outputX', setR + '.valueX')
            pmc.setAttr(setR + '.oldMinX', 0)
            pmc.setAttr(setR + '.oldMaxX', 1)
            pmc.setAttr(setR + '.minX', 0)
            pmc.setAttr(setR + '.maxX', numJoints)
            pmc.connectAttr(setR + '.outValueX', ctrl[0] + '.numberOfJointsAffected')

               
            paramU = pmc.getAttr(flcl[0] + '.parameterU')
            
            div_ten = pmc.createNode('multiplyDivide', n="DIV_" + name + controlPrefix + str(i+1))
            pmc.setAttr(div_ten.input2X, 10)
            pmc.setAttr(div_ten.operation, 2)

            pmc.connectAttr(ctrl[0] + '.position', div_ten.input1X)

            pmc.connectAttr(div_ten.outputX, flcl[0] + '.parameterU')

            pmc.setAttr(ctrl[0] + '.position', paramU * 10.0)
            
            fPos_plus = pmc.createNode('plusMinusAverage', n= name + 'fPosPlus_vfk_' + str(i+1))
            pmc.connectAttr(div_ten.outputX, fPos_plus + '.input1D[0]', f=True)
            pmc.connectAttr(ctrl[0] + '.falloff', fPos_plus + '.input1D[1]', f=True)
            pmc.setAttr(fPos_plus + '.operation', 1)
            
            fPos_minus = pmc.createNode('plusMinusAverage', n=  name + 'fPosMinus_vfk_' + str(i+1))
            pmc.connectAttr(div_ten.outputX, fPos_minus + '.input1D[0]', f=True)
            pmc.connectAttr(ctrl[0] + '.falloff', fPos_minus + '.input1D[1]', f=True)
            pmc.setAttr(fPos_minus + '.operation', 2)
            
            for f in (fPos_plus, fPos_minus):
                for j in xrange(len(joints)):
                    upperM = pmc.createNode('plusMinusAverage', n= (name + f + '_upperM_j' + str(j+1) + '_c' + str(i+1)))
                    lowerM = pmc.createNode('plusMinusAverage', n= (name + f + '_lowerM_j' + str(j+1) + '_c' + str(i+1)))
                    
                    pmc.setAttr(upperM + '.operation', 2)
                    pmc.setAttr(lowerM + '.operation', 2)
                    
                    pmc.connectAttr(joints[j] + '.position', upperM + '.input1D[0]')
                    pmc.connectAttr(f + '.output1D', upperM + '.input1D[1]')
                    
                    pmc.connectAttr(div_ten.outputX, lowerM + '.input1D[0]')
                    pmc.connectAttr(f + '.output1D', lowerM + '.input1D[1]')
                    
                    divA = pmc.createNode('multiplyDivide', n= f + '_divA_j' + str(j+1) + '_c' + str(i+1))
                    pmc.setAttr(divA + '.operation', 2)
                    pmc.connectAttr(upperM + '.output1D', divA + '.input1X')
                    pmc.connectAttr(lowerM + '.output1D', divA + '.input2X')
                    
                    multA = pmc.createNode('multiplyDivide', n= f + '_multA_j' + str(j+1) + '_c' + str(i+1))
                    pmc.setAttr(multA + '.operation', 1)
                    pmc.connectAttr(divA + '.outputX', multA + '.input1X')
                    pmc.setAttr(multA + '.input2X', 2)

                    divB = pmc.createNode('multiplyDivide', n= f + '_divB_j' + str(j+1) + '_c' + str(i+1))
                    pmc.setAttr(divB + '.operation', 2)
                    pmc.connectAttr(multA + '.outputX', divB + '.input1X')
                    pmc.connectAttr(ctrl[0] + '.numberOfJointsAffected', divB + '.input2X')
                    
                    
            for j in xrange(len(joints)):
                cond = pmc.createNode('condition', n= name + 'cond_j' + str(j+1) + '_c' + str(i+1))
                pmc.setAttr(cond + '.operation', 3)
                pmc.connectAttr(div_ten.outputX, cond + '.firstTerm') # then use minus
                pmc.connectAttr(joints[j] + '.position', cond + '.secondTerm') # then use plus

                pmc.connectAttr(fPos_minus + '_divB_j' + str(j+1) + '_c' + str(i+1) + '.outputX', cond + '.colorIfTrueR')
                pmc.connectAttr(fPos_minus + '_divB_j' + str(j+1) + '_c' + str(i+1) + '.outputX', cond + '.colorIfTrueG')
                pmc.connectAttr(fPos_minus + '_divB_j' + str(j+1) + '_c' + str(i+1) + '.outputX', cond + '.colorIfTrueB')

                pmc.connectAttr(fPos_plus + '_divB_j' + str(j+1) + '_c' + str(i+1) + '.outputX', cond + '.colorIfFalseR')
                pmc.connectAttr(fPos_plus + '_divB_j' + str(j+1) + '_c' + str(i+1) + '.outputX', cond + '.colorIfFalseG')
                pmc.connectAttr(fPos_plus + '_divB_j' + str(j+1) + '_c' + str(i+1) + '.outputX', cond + '.colorIfFalseB')
                
                cond_neg = pmc.createNode('condition', n= name + 'cond_neg_j' + str(j+1) + '_c' + str(i+1))
                pmc.connectAttr(cond + '.outColorR', cond_neg + '.firstTerm')
                pmc.setAttr(cond_neg + '.secondTerm', 0)
                pmc.setAttr(cond_neg + '.operation', 2)
                pmc.connectAttr(cond + '.outColor', cond_neg + '.colorIfTrue')
                pmc.setAttr(cond_neg + '.colorIfFalse', [0,0,0])
                
                multiFinalRot = pmc.createNode('multiplyDivide', n=  name + 'multiFinalRot_j' + str(j+1) + '_c' + str(i+1))
                pmc.setAttr(multiFinalRot + '.operation', 1)
                pmc.connectAttr(cond_neg + '.outColor', multiFinalRot + '.input1')
                pmc.connectAttr(ctrl[0] + '.rotate', multiFinalRot + '.input2')
                
                pmc.connectAttr(multiFinalRot + '.output', name + jointGroupPrefix + 'j' + str(j+1) + '_c' + str(i+1) + '.rotate')

                '''
                multiFinalScl = pmc.createNode('multiplyDivide', n=  name + 'multiFinalScl_j' + str(j+1) + '_c' + str(i+1))
                pmc.setAttr(multiFinalScl + '.operation', 1)
                pmc.connectAttr(cond + '.outColor', multiFinalScl + '.input1')
                pmc.connectAttr(ctrl[0] + '.scale', multiFinalScl + '.input2')
                
                pmc.connectAttr(multiFinalScl + '.output', name + jointGroupPrefix + 'j' + str(j+1) + '_c' + str(i+1) + '.scale')
                '''
            self._ctrlDBL(ctrl)
        
        if endChild:
            pmc.parent(linkJointEnd, endJoint)
 
        pmc.undoInfo(closeChunk=True)
        pmc.undoInfo(openChunk=True)
            
        pmc.skinCluster(joints, name + 'vfk_surface', mi=1)
        
        pmc.undoInfo(closeChunk=True)
        

    ####################
    # INTERNAL FUNCTIONS
    ####################
    def _jointRes(self, parentJoint, endJoint, boneTranslateAxis = '.tx', add=2.0, name="subJoint_"):
        pmc.undoInfo(openChunk=True)
        
        selJoints = pmc.ls(selection=True)
        
        boneLength = mc.getAttr(endJoint + boneTranslateAxis)
        boneRadius = mc.getAttr(parentJoint + ".radius")

        mc.select(cl=True)
        
        for i in xrange(int(round(add))):
            newJoint = pmc.joint(name=name + str(i+1), radius = (boneRadius*2))
            mc.select(cl=True)
            pmc.parent(newJoint, parentJoint, relative=True)
            mc.setAttr(newJoint + boneTranslateAxis, (boneLength/(add + 1)))
            if i > 0:
                pmc.parent(newJoint, (name + str(i)), relative = True)
            if i == add - 1:
                pmc.parent(endJoint, newJoint)
        
        pmc.undoInfo(closeChunk=True)
    
    
    def _parentSurfaceFLCL(self, constrained_obj, geo, deleteCPOMS=1):
        """
        Parents object to follicle at closest point on surface. 
        Select child transform, then select mesh to hold parent follicle. 
        
        """
        cpos = pmc.createNode('closestPointOnSurface', n='cpos_flcl_' + geo)

        mc.connectAttr(pmc.listRelatives(geo, shapes=True, children=True)[0] + '.local', cpos + '.inputSurface')
        obj_mtx = pmc.xform(constrained_obj, q=True, m=True)
        pmc.setAttr(cpos + '.inPosition', [obj_mtx[12], obj_mtx[13], obj_mtx[14]])

        flclShape = pmc.createNode('follicle', n='flclShape' + geo)
        flcl = pmc.listRelatives(flclShape, type='transform', parent=True)
        pmc.rename(flcl, 'flcl_' + geo + '_1')

        mc.connectAttr(flclShape + '.outRotate', flcl[0] + '.rotate')
        mc.connectAttr(flclShape + '.outTranslate', flcl[0] + '.translate')
        mc.connectAttr(geo + '.worldMatrix', flclShape + '.inputWorldMatrix')
        mc.connectAttr(geo + '.local', flclShape + '.inputSurface')
        mc.setAttr(flclShape + '.simulationMethod', 0)

        u = mc.getAttr(cpos + '.result.parameterU')
        v = mc.getAttr(cpos + '.result.parameterV')
        pmc.setAttr(flclShape + '.parameterU', u)
        pmc.setAttr(flclShape + '.parameterV', v)

        pmc.parent(constrained_obj, flcl)
        if deleteCPOMS == 1:
            pmc.delete(cpos)
                
        return flcl

    ### offset double tranlate/rotate tranforms on a given control
    def _ctrlDBL(self, controls):
        
        pmc.undoInfo(openChunk=True)
        
        if controls == []:
            controls = pmc.ls(sl=True)

        for control in controls:
            control_roo = pmc.xform(control, q=True, roo=True)
            control_mtx = pmc.xform(control, q=True, m=True, ws=True)
            control_parent = pmc.listRelatives(control, p=True)
            pmc.select(cl=True)
            
            locdbl_parent = pmc.spaceLocator(n='locDBL_parent_' + control)
            locdbl_offset = pmc.spaceLocator(n='locDBL_offset_' + control)

            pmc.xform(locdbl_parent, ws=True, m=control_mtx)
            pmc.xform(locdbl_offset, ws=True, m=control_mtx)
                
            pmc.parent(locdbl_offset, locdbl_parent)
            pmc.parent(locdbl_parent, control_parent)
            pmc.parent(control, locdbl_offset)
            
            if control_roo == 'xyz':
                pmc.xform(locdbl_offset, roo='zyx')
            if control_roo == 'yzx':
                pmc.xform(locdbl_offset, roo='xzy')        
            if control_roo == 'zxy':
                pmc.xform(locdbl_offset, roo='yxz')        
            if control_roo == 'xzy':
                pmc.xform(locdbl_offset, roo='yzx')
            if control_roo == 'yxz':
                pmc.xform(locdbl_offset, roo='zxy')            
            if control_roo == 'zyx':
                pmc.xform(locdbl_offset, roo='xyz')
                            
            md_trns = pmc.createNode('multiplyDivide', n='mdTRNS_locDBL_' + control)
            md_rot = pmc.createNode('multiplyDivide', n='mdROT_locDBL_' + control)
            md_scl = pmc.createNode('multiplyDivide', n='mdSCL_locDBL_' + control)
            
            pmc.setAttr(md_trns + '.input1', [-1,-1,-1])
            pmc.setAttr(md_rot.input1, [-1,-1,-1])
            pmc.setAttr(md_scl.input1, [ 1, 1, 1])
            pmc.setAttr(md_scl.operation, 2)

            
            pmc.connectAttr(control + '.translate', md_trns + '.input2')
            pmc.connectAttr(control + '.rotate', md_rot + '.input2')
            pmc.connectAttr(control + '.scale', md_scl + '.input2')
            
            pmc.connectAttr(md_trns + '.output', locdbl_offset + '.translate')
            pmc.connectAttr(md_rot + '.output', locdbl_offset + '.rotate')
            pmc.connectAttr(md_scl + '.output', locdbl_offset + '.scale')
            
            pmc.setAttr(locdbl_parent + 'Shape.visibility', 0)
            pmc.setAttr(locdbl_offset + 'Shape.visibility', 0)
            
        pmc.undoInfo(closeChunk=True)
            


if __name__ == '__main__':
    try:
        vfk_ui.deleteLater()
    except:
        pass
    
    vfk_ui = VFK_UI()
    
    try:
        vfk_ui.create_ui()
        vfk_ui.show()
    except:
        vfk_ui.deleteLater()