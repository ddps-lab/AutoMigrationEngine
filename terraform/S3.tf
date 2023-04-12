data "aws_s3_bucket" "bucket" {
  bucket = "container-migration-log"
}

resource "aws_s3_bucket" "bucket" {
  # If the bucket already exists, the count will be zero, and the bucket will not be created.
  count = length(data.aws_s3_bucket.bucket) == 0 ? 1 : 0

  bucket = "container-migration-log"

  tags = {
    Name = "container-migration-log"
  }
}

resource "aws_s3_bucket_acl" "s3_acl" {
  count = length(aws_s3_bucket.bucket)

  bucket = aws_s3_bucket.bucket[count.index].id
  acl = "private"
}
