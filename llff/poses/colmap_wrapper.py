import os
import subprocess



# $ DATASET_PATH=/path/to/dataset

# $ colmap feature_extractor \
#    --database_path $DATASET_PATH/database.db \
#    --image_path $DATASET_PATH/images

# $ colmap exhaustive_matcher \
#    --database_path $DATASET_PATH/database.db

# $ mkdir $DATASET_PATH/sparse

# $ colmap mapper \
#     --database_path $DATASET_PATH/database.db \
#     --image_path $DATASET_PATH/images \
#     --output_path $DATASET_PATH/sparse

# $ mkdir $DATASET_PATH/dense
def run_colmap(basedir, match_type):
    
    # 执行几个colmap命令 输出到？
    logfile_name = os.path.join(basedir, 'colmap_output.txt')
    logfile = open(logfile_name, 'w')

    '''
    colmap feature_extractor --database_path /content/drive/My Drive/data/testscene3/database.db --image_path /content/drive/My Drive/data/testscene3/images --ImageReader.single_camera 1
./colmap feature_extractor --database_path /Users/mac/Downloads/fern1/database.db --image_path /Users/mac/Downloads/fern1/images --ImageReader.single_camera 1
feature_extractor，feature_importer：对一组图像执行特征提取或导入特征。
feature_extractor, feature_importer: Perform feature extraction or import features for a set of images.
    '''
    feature_extractor_args = [
        'colmap', 'feature_extractor', 
            '--database_path', os.path.join(basedir, 'database.db'), 
            '--image_path', os.path.join(basedir, 'images'),
            '--ImageReader.single_camera', '1',
            # '--SiftExtraction.use_gpu', '0',
    ]
    print('=======================')
    print(' '.join(feature_extractor_args))
    print('=======================')
    feat_output = ( subprocess.check_output(feature_extractor_args, universal_newlines=True) )
    logfile.write(feat_output)
    print('Features extracted')

    '''
    colmap exhaustive_matcher --database_path /content/drive/My Drive/data/testscene3/database.db
./colmap exhaustive_matcher --database_path /Users/mac/Downloads/fern1/database.db
exhaustive_matcher，vocab_tree_matcher，sequential_matcher， spatial_matcher，transitive_matcher，matches_importer：执行特征提取后进行特征匹配。
exhaustive_matcher, vocab_tree_matcher, sequential_matcher, spatial_matcher, transitive_matcher, matches_importer: Perform feature matching after performing feature extraction.
    '''
    exhaustive_matcher_args = [
        'colmap', match_type, 
            '--database_path', os.path.join(basedir, 'database.db'), 
    ]
    print('=======================')
    print(' '.join(exhaustive_matcher_args))
    print('=======================')
    match_output = ( subprocess.check_output(exhaustive_matcher_args, universal_newlines=True) )
    logfile.write(match_output)
    print('Features matched')
    
    p = os.path.join(basedir, 'sparse')
    if not os.path.exists(p):
        os.makedirs(p)

    # mapper_args = [
    #     'colmap', 'mapper', 
    #         '--database_path', os.path.join(basedir, 'database.db'), 
    #         '--image_path', os.path.join(basedir, 'images'),
    #         '--output_path', os.path.join(basedir, 'sparse'),
    #         '--Mapper.num_threads', '16',
    #         '--Mapper.init_min_tri_angle', '4',
    # ]

    '''
    colmap mapper --database_path /content/drive/My Drive/data/testscene3/database.db --image_path /content/drive/My Drive/data/testscene3/images --output_path /content/drive/My Drive/data/testscene3/sparse --Mapper.num_threads 16 --Mapper.init_min_tri_angle 4 --Mapper.multiple_models 0 --Mapper.extract_colors 0
./colmap mapper --database_path /Users/mac/Downloads/fern1/database.db --image_path /Users/mac/Downloads/fern1/images --output_path /Users/mac/Downloads/fern1/sparse --Mapper.num_threads 12 --Mapper.init_min_tri_angle 4 --Mapper.multiple_models 0 --Mapper.extract_colors 0
mapper：执行特征提取和匹配后，使用SfM稀疏地对数据集进行3D重建/映射。
mapper: Sparse 3D reconstruction / mapping of the dataset using SfM after performing feature extraction and matching.
    '''
    mapper_args = [
        'colmap', 'mapper',
            '--database_path', os.path.join(basedir, 'database.db'),
            '--image_path', os.path.join(basedir, 'images'),
            '--output_path', os.path.join(basedir, 'sparse'), # --export_path changed to --output_path in colmap 3.6
            '--Mapper.num_threads', '16',
            '--Mapper.init_min_tri_angle', '4',
            '--Mapper.multiple_models', '0',
            '--Mapper.extract_colors', '0',
    ]
    print('=======================')
    print(' '.join(mapper_args))
    print('=======================')
    map_output = ( subprocess.check_output(mapper_args, universal_newlines=True) )
    logfile.write(map_output)
    logfile.close()
    print('Sparse map created')
    
    print( 'Finished running COLMAP, see {} for logs'.format(logfile_name) )


