pro set_path
cd, current=current_dir
split_dir = STRSPLIT(current_dir, '/', /EXTRACT)
indx = WHERE(split_dir eq 'R136', /null)
start_dir = '/'+STRJOIN(split_dir[0:indx[0]], '/')

!path=start_dir+'/'+'/multispec/code/:'+!path
!path=start_dir+'/'+'/multispec/chorizos/:'+!path
!path=start_dir+'/'+'/multispec/jmaplot/:'+!path
end
